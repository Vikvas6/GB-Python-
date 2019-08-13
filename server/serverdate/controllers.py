from protocol import make_response
from datetime import datetime

def date_controller(request):
    return make_response(
        200, request, datetime.now().timestamp()
    )