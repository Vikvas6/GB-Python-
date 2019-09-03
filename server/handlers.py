import json
import logging

from resolvers import resolve
from protocol import validate_request, make_response
from middlewares import compression_middleware

@compression_middleware
def handle_tcp_request(bytes_request):
    request = json.loads(bytes_request.decode())

    if validate_request(request):
        action = request.get('action')
        controller = resolve(action)
        if controller:
            try:
                response = controller(request)
                logging.debug(f'Client sent message {request}')
            except Exception as err:
                response = make_response(
                    500, request, f'Internal server error')
                logging.critical(f'Exception - {err}')
        else:
            response = make_response(
                404, request, f'Action {action} not implemented')
            logging.error(f'Client sent action {action}')
    else:
        response = make_response(400, request, 'Wrong request')
        logging.error(f'Client sent wrong request')

    string_response = json.dumps(response)
    return string_response.encode()