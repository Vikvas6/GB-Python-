import pytest

from echo.controllers import echo_controller

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

def test_code_echo_controller(request_msg, expected_code):
    actual_request = echo_controller(request_msg)
    assert actual_request.get('code') == expected_code

def test_request_echo_controller(request_msg, initial_action):
    actual_request = echo_controller(request_msg)
    assert actual_request.get('action') == initial_action

 
    
