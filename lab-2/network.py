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
    with open(HMAC_keyfile, "r") as h, open(DES_keyfile, "r") as d:
        local_HMACkey = h.read()
        local_DESkey = d.read()
        d.close()
        h.close()

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f'Welcome! You are the client! Press {EXIT_KEY} to exit at your turn...\n')

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
        client_socket.send(client_send, str.encode(local_hmac))
            # needs to send ciphertext, message, and hmac

        # wait...
        # get new output from the server
        recv_data = client_socket.recv(RECV_BYTES)

        # decrypt message
        client_recv = recv_data.decode()    # decrypt method

        # start over, send new input
        client_input = input(INPUT_STR)

    client_socket.close()
    sys.exit()

def server_program():
    with open(HMAC_keyfile, "r") as h, open(DES_keyfile, "r") as d:
        local_HMACkey = h.read()
        local_DESkey = d.read()
        d.close()
        h.close()

    server_socket = socket(AF_INET, SOCK_STREAM)
    print('\nWelcome! Please wait until client connects...')

    server_socket.bind((HOST, PORT))
    server_socket.listen(BACKLOG)
    conn, addr = server_socket.accept()

    print(f'--> Connected with client, address {repr(addr)}\n')
    while True:
        recv_data, recv_hmac = conn.recv(RECV_BYTES)
        if not recv_data:
            print(f'{EXIT_KEY} was sent by {CLIENT}. Program terminated.')
            break

        print("ONE: ", recv_data)
        print("TWO: ", recv_hmac)

        # decode messages
        server_recv = recv_data
        given_hmac = recv_hmac
            # use .decode() for decrypting DES

        # calculate
        calculated_hmac = None
            # FIX THIS LATER

        # decrypt everything
        given_msg = descrypt(DEC, local_DESkey)
        format_msg(
            True,
            server_recv,
            given_msg,
            given_hmac,
            calculated_hmac
        )

        # send input back
        server_msg = input(INPUT_STR)

        # encrypt message
        server_send = None      # encrypt
        conn.send(server_send)

    conn.close()