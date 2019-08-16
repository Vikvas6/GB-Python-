import pytest

from serverdate.controllers import date_controller

@pytest.fixture
def initial_action():
    return 'test'

@pytest.fixture
def request_msg(initial_action):
    return {
        'action': initial_action
    }

@pytest.fixture
def expected_code():
    return 200

def test_code_date_controller(request_msg, expected_code):
    actual_request = date_controller(request_msg)
    assert actual_request.get('code') == expected_code

def test_request_date_controller(request_msg, initial_action):
    actual_request = date_controller(request_msg)
    assert actual_request.get('action') == initial_action

 
    
