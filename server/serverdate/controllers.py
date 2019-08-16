from protocol import make_response
from datetime import datetime

def date_controller(request):
    return make_response(
        200, request, datetime.now().timestamp()
    )

def get_human_date(request):
    dt = datetime.now()
    string_dt = dt.strftime('%Y-%m-%d %H:%M')
    return make_response(
        200, request, string_dt
    )