import socket
import yaml
from argparse import ArgumentParser
import json
import logging

from resolvers import resolve
from protocol import validate_request, make_response


config = {
    'addr': '127.0.0.1',
    'port': 7777,
    'buffersize': 1024
}

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False,
    help='Sets config file path'
)
parser.add_argument(
    '-a', '--addr', type=str, required=False,
    help='Sets server address (host)'
)
parser.add_argument(
    '-p', '--port', type=int, required=False,
    help='Sets server port'
)

args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        file_config = yaml.safe_load(file)
        config.update(file_config or {})

if args.addr:
    config['addr'] = args.addr

if args.port:
    config['port'] = args.port

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=(
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    )
)


def recieve_msg(client):
    return json.loads(client.recv(config.get('buffersize')).decode())


def send_msg(sock, data):
    sock.send(json.dumps(data).encode())


try:
    sock = socket.socket()
    sock.bind((config.get('addr'), config.get('port')))
    sock.listen(5)

    logging.info(
        f'Server started on {config.get("addr")}:{config.get("port")}')

    while True:
        client, address = sock.accept()
        client_host, client_port = address
        logging.info(f'Client was detected on {client_host}:{client_port}')

        request = recieve_msg(client)

        if validate_request(request):
            action = request.get('action')
            controller = resolve(action)
            if controller:
                try:
                    response = controller(request)
                    logging.debug(
                        f'Client {client_host}:{client_port} sent message {request.get("data")}')
                except Exception as err:
                    response = make_response(
                        500, request, f'Internal server error')
                    logging.critical(f'Exception - {err}')
            else:
                response = make_response(
                    404, request, f'Action {action} not implemented')
                logging.error(
                    f'Client {client_host}:{client_port} sent action {action}')
        else:
            response = make_response(400, request, 'Wrong request')
            logging.error(
                f'Client {client_host}:{client_port} sent wrong request')
        send_msg(client, response)

        client.close()
except KeyboardInterrupt:
    print('Server shutdown')
