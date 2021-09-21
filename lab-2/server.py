# server.py
# socket program for server

from configurations import *

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

        # calculate
        given_hmac = None
        calculated_hmac = None

        # decrypt everything
        given_msg = descrypt(DEC, local_DESkey, recv_data).decode()
        print("ACCEPTABLE: ", given_msg)
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
        conn.send(server_send)

    conn.close()