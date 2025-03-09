import os

import pytest
from aiohttp import ClientSession

from emerald_ems.api import EmeraldApiClient


@pytest.mark.integration
async def it_should_login_with_valid_credentials():
	email = os.getenv('EMERALD_EMS_EMAIL')
	password = os.getenv('EMERALD_EMS_PASSWORD')

	async with ClientSession() as session:
		api = EmeraldApiClient(email, password, session)
		data = await api.sign_in()

	assert 'email' in data
	assert data['email'] == email
