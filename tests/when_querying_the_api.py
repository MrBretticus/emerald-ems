import re

from datetime import date

import pytest

from aiohttp import ClientError
from aioresponses import aioresponses

from emerald_ems.api import EmeraldApiClient
from emerald_ems.const import (
	SIGN_IN_URL,
	PROPERTY_LIST_URL,
	PROPERTY_INFO_URL,
	DEVICE_FLASHES_URL
)
from emerald_ems.exceptions import (
	EmeraldApiClientAuthenticationError,
	EmeraldApiClientCommunicationError,
	EmeraldApiClientError
)

from .payloads import TGetPayload
from .sign_in import TSignIn


EXAMPLE_PROPERTY_ID = 1
EXAMPLE_DEVICE_ID = 1
EXAMPLE_START_DATE = date(2023, 12, 1)
EXAMPLE_END_DATE = date(2023, 12, 2)


async def it_should_login_with_valid_credentials(sign_in:TSignIn):
	data = await sign_in()

	assert 'email' in data

async def it_should_fail_login_with_invalid_credentials(responses:aioresponses, sign_in:TSignIn):
	responses.post(
		url=SIGN_IN_URL,
		status=401,
		reason='Unauthorized'
	)

	with pytest.raises(EmeraldApiClientAuthenticationError):
		await sign_in()

async def it_should_handle_communication_errors(responses:aioresponses, sign_in:TSignIn):
	responses.post(
		url=SIGN_IN_URL,
		exception=ClientError()
	)

	with pytest.raises(EmeraldApiClientCommunicationError):
		await sign_in()

async def it_should_handle_generic_errors(responses:aioresponses, sign_in:TSignIn):
	responses.post(
		url=SIGN_IN_URL,
		exception=Exception()
	)

	with pytest.raises(EmeraldApiClientError):
		await sign_in()

@pytest.mark.usefixtures('auto_sign_in')
async def it_should_list_properties(responses:aioresponses, client:EmeraldApiClient, get_payload:TGetPayload):
	payload = get_payload('property_list.json')

	responses.get(
		url=PROPERTY_LIST_URL,
		status=200,
		payload=payload
	)

	data = await client.list_properties()

	assert data == payload['info']['property']

@pytest.mark.usefixtures('auto_sign_in')
async def it_should_get_property_info(responses:aioresponses, client:EmeraldApiClient, get_payload:TGetPayload):
	payload = get_payload('property_info.json')

	responses.get(
		url=f'{PROPERTY_INFO_URL}?property_id={EXAMPLE_PROPERTY_ID}',
		status=200,
		payload=payload
	)

	data = await client.get_property(EXAMPLE_PROPERTY_ID)

	assert data == payload['property_list']

@pytest.mark.usefixtures('auto_sign_in')
async def it_should_get_device_flashes(responses:aioresponses, client:EmeraldApiClient, get_payload:TGetPayload):
	payload = get_payload('device_flashes.json')
	url_pattern = DEVICE_FLASHES_URL.replace(".", "\\.")

	responses.get(
		url=re.compile(rf'^{url_pattern}\?.*$'),
		status=200,
		payload=payload
	)

	data = await client.get_device_flashes(
		EXAMPLE_DEVICE_ID,
		EXAMPLE_START_DATE,
		EXAMPLE_END_DATE
	)

	assert data == payload['info']
