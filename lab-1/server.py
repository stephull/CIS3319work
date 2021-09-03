'''
    server.py       -- Main program for server (socket programming)
'''

from configurations import *
from gears import *

def server_side():
    print("Starting client-socket program...")

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((LOCALHOST, PORT))

    server_socket.listen(BACKLOG)
    conn, addr = server_socket.accept()

    print(f'Connecting with client {str(addr)}\n')

    while True:
        data = conn.recv(RECV_BYTES).decode()
        if not data:
            print(f'Client has exited by typing {EXIT_KEY}, server shutting down.')
            break
        print(f'From client: {str(data)}')
        data = input(INPUT_STR)
        conn.send(data.encode())
    conn.close()

if __name__ == '__main__':
    server_side()