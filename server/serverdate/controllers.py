from protocol import make_response
from datetime import datetime
from decorators import logged


@logged('%(name)s - %(response)s')
def date_controller(request):
    return make_response(
        200, request, datetime.now().timestamp()
    )


@logged('%(name)s - %(response)s')
def get_human_date(request):
    dt = datetime.now()
    string_dt = dt.strftime('%Y-%m-%d %H:%M')
    return make_response(
        200, request, string_dt
    )
