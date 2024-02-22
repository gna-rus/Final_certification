import functools

import pytest
from Task1_sem4 import Site
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
