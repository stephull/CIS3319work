# client.py
# socket program for client

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
    client_socket.connect((HOST, PORT))
    print(f'Welcome! You are the client! Press {EXIT_KEY} to exit at your turn...\n')

    local_HMACkey = read_key(HMAC_keyfile)
    local_DESkey = read_key(DES_keyfile)

    client_input = input(INPUT_STR)
    while client_input.lower().strip() != EXIT_KEY:

        # assemble HMAC and encrypt message
        local_hmac = get_hmac(local_HMACkey, client_input)
        concat_input = concat(client_input, local_hmac)
        client_send = descrypt(ENC, local_DESkey, concat_input)
        format_msg(
            False, 
            local_DESkey, 
            local_HMACkey,
            client_input,
            local_hmac,
            client_send
        )
        client_socket.send(client_send)

        # wait...
        # get new output from the server
        recv_data = client_socket.recv(RECV_BYTES)
        given_hmac = None
        calculated_hmac = None

        # decrypt everything
        given_msg = descrypt(DEC, local_DESkey, recv_data).decode()
        format_msg(
            True,
            recv_data,
            given_msg,
            given_hmac,
            calculated_hmac
        )

        # start over, send new input
        client_input = input(INPUT_STR)

    client_socket.close()
    sys.exit()