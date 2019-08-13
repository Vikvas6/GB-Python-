from datetime import datetime

def validate_request(request):
    if 'action' in request and 'time' in request:
        return True
    else:
        return False
def make_response(code, request_msg, data):
    response_msg = {
        'code': code,
        'data': data,
        'time': datetime.now().timestamp()
    }
    return response_msg