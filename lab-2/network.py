# socket.py
# socket program for client and server

from configurations import *

# show the server side of the socket program
def server_program():
    server_socket = socket(AF_INET, SOCK_STREAM)
    print('\nWelcome! Please wait until client connects...')

    server_socket.bind((HOST, PORT))
    server_socket.listen(BACKLOG)
    conn, addr = server_socket.accept()

    if conn: 
        local_HMACkey = read_key(HMAC_keyfile)
        local_DESkey = read_key(DES_keyfile)

    print(f'--> Connected with client, address {repr(addr).strip("()")}\n')
    while True:
        recv_data = conn.recv(RECV_BYTES)
        if not recv_data:
            print(f'{EXIT_KEY} was sent by {CLIENT}. Program terminated.')
            break
        
        recv_decoded = descrypt(DEC, local_DESkey, recv_data).decode()
        given_msg, given_hmac = split_contents(recv_decoded)
        calculated_hmac = get_hmac(local_HMACkey, given_msg)
        format_msg(
            True,
            recv_data,
            given_msg,
            given_hmac,
            calculated_hmac
        )

        # send input back
        server_input = input(INPUT_STR)

        # encrypt message
        local_hmac = get_hmac(local_HMACkey, server_input)
        concat_input = concat(server_input, local_hmac)
        server_send = descrypt(ENC, local_DESkey, concat_input)
        format_msg(
            False, 
            local_DESkey, 
            local_HMACkey,
            server_input,
            local_hmac,
            server_send
        )
        conn.send(server_send)

    conn.close()

# show the client side of the program
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

        recv_decoded = descrypt(DEC, local_DESkey, recv_data).decode()
        given_msg, given_hmac = split_contents(recv_decoded)
        calculated_hmac = get_hmac(local_HMACkey, given_msg)
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