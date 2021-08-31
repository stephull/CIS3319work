'''
    server.py       -- Main program for server (socket programming)
'''

from configurations import *
from socket import *

# create new server
def start_server():
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((LOCALHOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Accepted new connection from {}'.format(addr))
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
