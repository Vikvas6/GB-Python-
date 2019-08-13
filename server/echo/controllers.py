from protocol import make_response

def echo_controller(request):
    data = request.get('data')
    return make_response(200, request, data)