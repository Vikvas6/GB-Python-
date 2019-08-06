import socket
import yaml
from argparse import ArgumentParser
import json

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

def recieve_msg(client):
    request_msg = client.recv(config.get('buffersize')).decode()
    return request_msg

def create_response_msg(request_msg):
    request_dict = json.loads(request_msg)
    print(f'Client sent message code: {request_dict.get("code")}, data: {request_dict.get("data")}')
    return request_dict

def send_msg(sock, data):
    sock.send(json.dumps(data).encode())

if __name__ == '__main__':
    try:
        sock = socket.socket()
        sock.bind((config.get('addr'), config.get('port')))
        sock.listen(5)

        print(f'Server started on {config.get("addr")}:{config.get("port")}')

        while True:
            client, address = sock.accept()
            client_host, client_port = address
            print(f'Client was detected on {client_host}:{client_port}')

            rec_msg = recieve_msg(client)
            res_msg = create_response_msg(rec_msg)
            send_msg(client, res_msg)

            client.close()
    except KeyboardInterrupt:
        print('Server shutdown')