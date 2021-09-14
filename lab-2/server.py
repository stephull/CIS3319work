# server.py
# socket program for server-side usage

from configurations import *

def server_program():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(HOST, PORT)
    server_socket.listen(BACKLOG)
    conn, addr = server_socket.accept()

    print(f'* Connected with: {str(addr)}\n')
    while True:
        receive_data = conn.recv(RECV_BYTES)
        if not receive_data:
            print(f'{EXIT_KEY} was sent by {CLIENT}. Program terminated.')
            break

        # decrypt message

        # send input back

        # encrypt message

    conn.close()