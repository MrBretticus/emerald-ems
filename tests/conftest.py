import os
import logging

import pytest
from dotenv import load_dotenv


@pytest.fixture(autouse=True)
def auto_enable_local_env():
	if os.path.exists(".env"):
		load_dotenv(os.path.abspath(".env"))

@pytest.fixture(autouse=True)
def init_logging():
	class PackageFilter(logging.Filter):
		def filter(self, record):
			return record.getMessage().startswith('emerald_ems')

	logging.getLogger().addFilter(PackageFilter())

def pytest_addoption(parser:pytest.Parser):
    parser.addoption("--use-response-files", action="store_true", help="")


# load fixtures from other files
pytest_plugins = 'tests.payloads,tests.sign_in'
