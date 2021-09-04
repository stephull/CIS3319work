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
        # receive data, which represents the encrypted message from the client
        data = conn.recv(RECV_BYTES).decode()   ###
        if not data:
            print(f'Client has exited by typing {EXIT_KEY}, server shutting down.')
            break

        # decrypt message 
        with open(keyfile, "r") as k:
            key = k.read()
            new_plaintext = decrypt_msg(key, data)
            print(f'\nFROM: {CLIENT}')
            format_msg(key, data, new_plaintext, DEC)

            # send input to client
            new_data = input(INPUT_STR)
            
            # encrypt new message
            ciphertext = encrypt_msg(key, new_data)
            format_msg(key, new_data, ciphertext, ENC)
            conn.send(new_data.encode())

            k.close()
    conn.close()

if __name__ == '__main__':
    server_side()