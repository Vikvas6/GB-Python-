import socket
import yaml
from argparse import ArgumentParser
import json
import logging
import select
import threading

from resolvers import resolve
from handlers import handle_tcp_request
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

requests = []
connections = []


def read(sock, connection, request, buffersize):
    try:
        bytes_request = sock.recv(buffersize)
    except Exception:
        connection.remove(sock)
    else:
        requests.append(bytes_request)


def write(sock, connection, response):
    try:
        sock.send(response)
    except Exception:
        connection.remove(sock)


try:
    sock = socket.socket()
    sock.bind((config.get('addr'), config.get('port')))
    # sock.setblocking(False)
    sock.settimeout(1)
    sock.listen(5)

    logging.info(
        f'Server started on {config.get("addr")}:{config.get("port")}')

    while True:
        try:
            client, address = sock.accept()
            client_host, client_port = address
            logging.info(f'Client was detected on {client_host}:{client_port}')
            connections.append(client)
        except:
            pass

        if connections:
            rlist, wlist, xlist = select.select(connections, connections, connections, 0)

            for read_client in rlist:
                read_thread = threading.Thread(daemon=True, target=read, args=(
                    read_client, connections, requests, config.get('buffersize')
                ))
                read_thread.start()

            if requests:
                bytes_request = requests.pop()
                bytes_response = handle_tcp_request(bytes_request)
            
                for write_client in wlist:
                    write_thread = threading.Thread(target=write, args=(
                        write_client, connections, bytes_response
                    ))
                    write_thread.start()
except KeyboardInterrupt:
    print('Server shutdown')
