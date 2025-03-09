import os

from json import load
from typing import Callable

import pytest

from jsf import JSF


type TGetPayload = Callable[[str], str]


def load_payload(filename:str):
	filePath = f'tests/payloads/{filename}'

	if os.path.exists(filePath):
		with open(filePath, encoding='utf-8') as fp:
			return load(fp)
	
	raise FileNotFoundError(f'{filePath} not found, you probably missing the example responses')
	
def generate_payload(schema_filename:str):
	return JSF.from_json(f'emerald_ems/schemas/{schema_filename}').generate()

@pytest.fixture
def get_payload(pytestconfig:pytest.Config) -> TGetPayload:
	def func(filename:str) -> str:
		return load_payload(filename) \
			if pytestconfig.getoption('use_response_files') \
				else generate_payload(filename)
	
	return func
