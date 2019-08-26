import pytest

from protocol import validate_request

@pytest.fixture
def valid_request():
    return {
        'action': 'test',
        'time': 'Some time'
    }

@pytest.fixture
def invalid_request_no_time():
    return {
        'action': 'test'
    }

@pytest.fixture
def invalid_request_no_action():
    return {
        'time': 'Some time'
    }

@pytest.fixture
def invalid_request_nothing():
    return {
    }

def test_valid_validate_request(valid_request):
    assert validate_request(valid_request)

def test_no_time_validate_request(invalid_request_no_time):
    assert not validate_request(invalid_request_no_time)

def test_no_action_validate_request(invalid_request_no_action):
    assert not validate_request(invalid_request_no_action)

def test_nothing_validate_request(invalid_request_nothing):
    assert not validate_request(invalid_request_nothing)
