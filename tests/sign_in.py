from typing import Callable, Awaitable

import pytest

from aiohttp import ClientSession
from aioresponses import aioresponses
from emerald_ems.api import EmeraldApiClient
from emerald_ems.const import SIGN_IN_URL

from .payloads import TGetPayload


type TSignIn = Callable[[], Awaitable[str]]


@pytest.fixture
async def client():
	async with ClientSession() as session:
		yield EmeraldApiClient(session)

@pytest.fixture
def responses():
	with aioresponses() as responses:
		yield responses

@pytest.fixture
async def sign_in(client:EmeraldApiClient, responses:aioresponses, get_payload:TGetPayload) -> TSignIn:
	payload = get_payload('sign_in.json')
	
	async def do_sign_in() -> str:
		responses.post(
			url=SIGN_IN_URL,
			payload=payload
		)

		data = await client.sign_in("", "")
	
		return data
	
	return do_sign_in

@pytest.fixture
async def auto_sign_in(sign_in:TSignIn):
	await sign_in()
