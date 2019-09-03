import socket
import yaml
import zlib
from argparse import ArgumentParser
import json
from datetime import datetime
import threading

READ_MODE = 'read'
WRITE_MODE = 'write'

config = {
    'addr': '127.0.0.1',
    'port': 7777,
    'buffersize': 1024,
    'user': 'Vasya'
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

'''
Code    Data    Meaning
1       User    User is online
2       User    User is offline
3       Text    Send message to server
'''
def create_presence_msg(online=True):
    if online:
        action = 'presence.online'
    else:
        action = 'presence.offline'
    return {
        'code': 200,
        'data': config.get('user'),
        'action': action,
        'time': datetime.now().timestamp()
    }

def create_msg(action, data):
    #data = input('Enter data to send: ')
    return {
        'data': data,
        'action': action,
        'time': datetime.now().timestamp()
    }

def send_msg(sock, data):
    string_request = json.dumps(data)
    bytes_request = zlib.compress(string_request.encode())

    sock.send(bytes_request)

def get_response(sock, buffersize):
    compressed_response = sock.recv(buffersize)
    bytes_response = zlib.decompress(compressed_response)
    return bytes_response.decode()

def parse_response(resp):
    print(resp)


def read(sock, buffersize):
    while True:
        parse_response(get_response(sock, buffersize))


if __name__ == '__main__':
    try:
        sock = socket.socket()
        sock.connect((config.get('addr'), config.get('port')))

        print('Client was started')

        thread = threading.Thread(target=read, args=(sock, config.get('buffersize')))
        thread.start()

        while True:
            action  = input('Enter action to send: ')
            data = input('Enter data to send: ')
            send_msg(sock, create_msg(action, data))
            print('Client sent data')
                

    except KeyboardInterrupt:
        #send_msg(sock, create_presence_msg(False))
        print('Client shutdown')