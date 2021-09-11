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
    client_msg = input(INPUT_STR)

    key = make_key()

    # exit program by typing "-1" or pressing the 'Esc' key:
    while client_msg.lower().strip() != str(EXIT_KEY):

        # read from the file and encrypt message
        client_send = cipher(key, client_msg, ENC)
        format_msg(key, client_msg, client_send, ENC)
        client_socket.send(client_send)

        # wait until the server sends input...
        # receive new output from server
        receive_data = client_socket.recv(RECV_BYTES)

        # decrypt + message 
        client_recieve = cipher(key, receive_data, DEC).decode()
        print(f'\nFROM: {SERVER}')
        format_msg(key, receive_data, client_recieve, DEC)

        # send brand new input to server
        client_msg = input(INPUT_STR)

    client_socket.close()
    sys.exit()