# client.py
# socket program for client-side usage

from configurations import *

def client_program():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(HOST, PORT)

    client_input = input(INPUT_STR)
    while client_input.lower().strip() != EXIT_KEY:
        pass

        # encrypt message

        # wait
        # get new output from the server

        # decrypt message

        # start over, send new input

    client_socket.close()
    sys.exit()
