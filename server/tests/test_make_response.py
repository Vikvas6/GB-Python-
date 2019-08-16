import pytest
from datetime import datetime

from protocol import make_response

@pytest.fixture
def initial_action():
    return 'test'

@pytest.fixture
def initial_code():
    return 200

@pytest.fixture
def initial_data():
    return 'Some data'

@pytest.fixture
def initial_request(initial_action, initial_data):
    return {
        'action': initial_action,
        'time': datetime.now().timestamp(),
        'data': initial_data
    }


INITIAL_CODE = 200
INITIAL_DATA = 'Some data'
INITIAL_REQUEST = {
    'action': 'test',
    'time': datetime.now().timestamp(),
    'data': 'Some data'
}

EXPECTED_CODE = 200
EXPECTED_ACTION = 'test'
EXPECTED_DATA = 'Some data'

def test_action_make_response(initial_request, initial_code, initial_data, initial_action):
    actual_response = make_response(initial_code, initial_request, initial_data)
    assert actual_response.get('action') == initial_action

def test_code_make_response(initial_request, initial_code, initial_data):
    actual_response = make_response(initial_code, initial_request, initial_data)
    assert actual_response.get('code') == initial_code

def test_data_make_response(initial_request, initial_code, initial_data):
    actual_response = make_response(initial_code, initial_request, initial_data)
    assert actual_response.get('data') == initial_data
