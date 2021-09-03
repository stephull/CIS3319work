'''
    client.py       -- Main program for client (socket programming)
'''

from configurations import *
from socket import *
from select import *

def client_side():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((LOCALHOST, PORT))

    print(f'Welcome. You are the client. Remember to type {EXIT_KEY} to exit...')
    msg = input(INPUT_STR)

    # exit program by typing "-1" or pressing the 'Esc' key:
    while msg.lower().strip() != str(EXIT_KEY):
        client_socket.send(msg.encode())
        data = client_socket.recv(RECV_BYTES).decode()
        print(f'From server: {data}')
        msg = input(INPUT_STR)
    client_socket.close()
    sys.exit()

if __name__ == '__main__':
    client_side()