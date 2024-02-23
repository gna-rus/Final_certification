import functools

import pytest
from final_certification import Site
import yaml
import json
import requests

with open('data.yaml') as f:
    testdata = yaml.safe_load(f)

@pytest.fixture(scope="session")
def site_connect():
    site_instance = Site(testdata["browser"],testdata['addres'])
    yield site_instance
    site_instance.close()

@pytest.fixture()
def command_nikto():
    return 'nikto -h https://test-stand.gb.ru/ -ssl -Tuning 4'
