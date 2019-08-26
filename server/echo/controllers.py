from protocol import make_response

from decorators import logged


@logged('%(name)s - %(response)s')
def echo_controller(request):
    data = request.get('data')
    return make_response(200, request, data)
