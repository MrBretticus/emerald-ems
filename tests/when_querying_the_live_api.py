import os

import pytest

from emerald_ems.api import EmeraldApiClient


@pytest.mark.integration
async def it_should_login_with_valid_credentials(client:EmeraldApiClient):
	email = os.getenv('EMERALD_EMS_EMAIL')
	password = os.getenv('EMERALD_EMS_PASSWORD')
	data = await client.sign_in(email, password)

	assert 'email' in data
	assert data['email'] == email
