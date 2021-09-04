'''
    client.py       -- Main program for client (socket programming)
'''

from configurations import *
from gears import *

def client_side():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((LOCALHOST, PORT))

    print(f'Welcome. You are the client. Remember to type {EXIT_KEY} to exit...')
    
    # send input to server
    msg = input(INPUT_STR)

    # exit program by typing "-1" or pressing the 'Esc' key:
    while msg.lower().strip() != str(EXIT_KEY):

        # read from the file and encrypt message
        with open(keyfile, "r") as k:
            key = k.read()
            ciphertext = encrypt_msg(key, msg) ###
            format_msg(key, msg, ciphertext, ENC)
            
            # send the input, should send ciphertext
            client_socket.send(str(ciphertext).encode()) ###

            # ...

            data = client_socket.recv(RECV_BYTES).decode()

            # decrypt + message 
            new_plaintext = decrypt_msg(key, data)
            print(f'\nFROM: {SERVER}')
            format_msg(key, data, new_plaintext, DEC)

            k.close()

        # send input to server
        msg = input(INPUT_STR)

    client_socket.close()
    sys.exit()

if __name__ == '__main__':
    client_side()