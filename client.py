import socket
import yaml
from argparse import ArgumentParser
import json
from datetime import datetime

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
    sock.send(json.dumps(data).encode())

def get_response(sock):
    return sock.recv(config.get('buffersize')).decode()

def parse_response(resp):
    resp_dict = json.loads(resp)
    print(resp_dict)


if __name__ == '__main__':
    try:
        while True:
            sock = socket.socket()
            sock.connect((config.get('addr'), config.get('port')))

            print('Client was started')

            # send_msg(sock, create_presence_msg())
            # print('Present message was sent')
            # print(f'Present message response: {get_response(sock)}')

            action  = input('Enter action to send: ')
            data = input('Enter data to send: ')
            send_msg(sock, create_msg(action, data))
            parse_response(get_response(sock))

            sock.close()
    except KeyboardInterrupt:
        #send_msg(sock, create_presence_msg(False))
        print('Client shutdown')