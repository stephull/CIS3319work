'''
    client.py       -- Main program for client (socket programming)
'''

from configurations import *
from gears import *

def client_side():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((LOCALHOST, PORT))

    keyfile = generate_keyfile(generate_key(KEY_LEN))

    print(f'Welcome. You are the client. Remember to type {EXIT_KEY} to exit...')
    msg = input(INPUT_STR)

    # exit program by typing "-1" or pressing the 'Esc' key:
    while msg.lower().strip() != str(EXIT_KEY):
        with open(keyfile, "r") as k:
            key = k.read()
            ciphertext = encrypt_msg(key, msg)
            format_msg(key, msg, ciphertext)
            k.close()
        client_socket.send(msg.encode())
        data = client_socket.recv(RECV_BYTES).decode()
        print(f'From server: {data}')
        msg = input(INPUT_STR)
    client_socket.close()
    sys.exit()

if __name__ == '__main__':
    client_side()