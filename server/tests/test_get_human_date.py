import pytest

from serverdate.controllers import get_human_date

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

def test_code_get_human_date(request_msg, expected_code):
    actual_request = get_human_date(request_msg)
    assert actual_request.get('code') == expected_code

def test_request_get_human_date(request_msg, initial_action):
    actual_request = get_human_date(request_msg)
    assert actual_request.get('action') == initial_action

 
    
