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

    key = make_key()

    while True:
        # receive data, which represents the encrypted message from the client
        receive_data = conn.recv(RECV_BYTES)   ### S(4/10)
        if not receive_data:
            print(f'Client has exited by typing {EXIT_KEY}, server shutting down.')
            break

        # decrypt message 
        server_receive = decrypt_msg(key, receive_data).decode()     ### S(5/10)

        print(f'\nFROM: {CLIENT}')
        format_msg(key, receive_data, server_receive, DEC)

        # send input to client
        server_msg = input(INPUT_STR)     ### S(6/10)
        
        # encrypt new message
        server_send = encrypt_msg(key, server_msg)    ### S(7/10)
        format_msg(key, server_msg, server_send, ENC) 
        conn.send(server_send)     ### S(8/10)

    conn.close()