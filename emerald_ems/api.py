from datetime import date
from urllib.parse import urlencode

import asyncio
import socket

from aiohttp import ClientSession, ClientError, ClientResponseError

from .const import (
	LOGGER,
	SIGN_IN_URL,
	PROPERTY_LIST_URL,
	PROPERTY_INFO_URL,
	DEVICE_FLASHES_URL
)
from .exceptions import (
	EmeraldApiClientError,
	EmeraldApiClientResponseError,
	EmeraldApiClientAuthenticationError,
	EmeraldApiClientAuthorisationError,
	EmeraldApiClientCommunicationError
)


class EmeraldApiClient:
	def __init__(
		self,
		session: ClientSession,
	) -> None:
		self._session = session
		self._headers = {
			'Accept': 'application/json',
			'Accept-Encoding': 'gzip, deflate, br'
		}

	async def sign_in(self, email:str, password:str) -> str:
		"""Sign-in using username & password and return the access token."""
		data = await self._api_wrapper(
			method="post",
			url=SIGN_IN_URL,
			headers=self._headers,
			data={
				'email': email,
				'password': password
			}
		)
		
		self._headers['Authorization'] = f'Bearer {data["token"]}'

		return data['info']
	
	async def list_properties(self) -> dict:
		data = await self._api_wrapper(
			method='get',
			url=PROPERTY_LIST_URL,
			headers=self._headers
		)

		return data['info']['property']
	
	async def get_property(self, property_id:int) -> dict:
		data = await self._api_wrapper(
			method='get',
			url=PROPERTY_INFO_URL,
			headers=self._headers,
			params={
				'property_id': property_id
			}
		)

		return data['property_list']
	
	async def get_device_flashes(self, device_id:int, start_date:date, end_date:date) -> dict:
		data = await self._api_wrapper(
			method='get',
			url=DEVICE_FLASHES_URL,
			headers=self._headers,
			params={
				'device_id': device_id,
				'start_date': start_date.isoformat(),
				'end_date': end_date.isoformat()
			}
		)

		return data['info']

	async def _api_wrapper(
		self,
		method: str,
		url: str,
		data: dict | None = None,
		headers: dict | None = None,
		params: dict | None = None
	) -> any:
		"""Get information from the API."""

		if params:
			url = f'{url}?{urlencode(params)}'

		try:
			LOGGER.info(f'{method} request to {url}, heaers: {headers}')

			if url != SIGN_IN_URL:
				assert 'Authorization' in headers, \
					'No authorization token set, have you forgot to sign-in?'
			
			#async with async_timeout.timeout(10):
			response = await self._session.request(
				method=method,
				url=url,
				headers=headers,
				json=data,
				raise_for_status=False
			)

			if response.content_type == 'application/json':
				json = await response.json()

			response.raise_for_status() # raise after request so we can inspect response
			
			return json
		except ClientResponseError as error:
			if error.status == 401:
				raise EmeraldApiClientAuthenticationError(
					"Authentication failed, check credentials",
				)
			if error.status == 403:
				raise EmeraldApiClientAuthorisationError(
					'Authorisation failed'
				)
			
			message:str = error.message

			if json and 'error' in json:
				message = json['error']['message']
			
			raise EmeraldApiClientResponseError(f'Error {error.status}: {message}')

		except asyncio.TimeoutError as exception:
			raise EmeraldApiClientCommunicationError(
				"Timeout error fetching information",
			) from exception
		except (ClientError, socket.gaierror) as exception:
			raise EmeraldApiClientCommunicationError(
				"Error fetching information",
			) from exception
		except AssertionError:
			raise
		except Exception as exception:  # pylint: disable=broad-except
			raise EmeraldApiClientError(
				str(exception)
			) from exception
