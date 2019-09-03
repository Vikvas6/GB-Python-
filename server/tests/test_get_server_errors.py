import pytest

from servererrors.controllers import get_server_errors

@pytest.fixture
def initial_action():
    return 'test'

@pytest.fixture
def request_msg(initial_action):
    return {
        'action': initial_action
    }

def test_get_server_errors(request_msg):
    try:
        get_server_errors(request_msg)
    except Exception as err:
        assert err.args[0] == 'Custom server error'
    else:
        assert False 
    
