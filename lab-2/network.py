# network.py
# socket program for both server and client

from configurations import *

# both sides need to show the following:
'''
    * shared keys for HMAC + DES
    * plaintext and HMAC before concatenation
    * ciphertext to be sent
    * received ciphertext
    * plaintext and HMAC after decryption + separation
    * receiver calculated HMAC, using HMAC key and received plain msg+
    * verification result (comparing two HMAC's)
'''

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