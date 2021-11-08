'''
    Network.py
    ::: Handles the socket program for client and server (TGS or auth. server) :::
'''
from configurations import *

# instructions for every program
temp = "\n>>> Log:    Start "
input_id_client = "Enter the client ID: \n"
input_id_auth = "Enter the TGS access ID (for auth. server): \n"
input_id_serv = "Enter the service provider ID: \n"
ticket_c_as = "Confirm ticket to proceed: \n"
key_c_as = "Enter key given to proceed: \n"
ticket_c_v = "Confirm ticket to proceed: \n"
key_c_v = "Enter key given to proceed: \n"

# does the input allow for program to continue running?
def check_send(conn, e):
    if str(e).lower().strip() != EXIT_KEY : return True
    conn.send(str.encode(EXIT_KEY))
    return False

# client program
def client_program():
    client_socket = socket(AF_INET, SOCK_STREAM)
    print(f'{temp}client. Waiting for servers to connect to program...\n')
    
    client_socket.bind((HOST, PORT))
    client_socket.listen(BACKLOG)
    conn, addr = client_socket.accept()

    if conn: 
        print(f"Connected to TEST server\n(Address: {repr(addr).strip('()')})\n")
        local_key_client = read_key(KEY_CLIENT)     # ensure C and AS share same key!
        local_key_auth = read_key(KEY_AUTH)
        local_key_serv = read_key(KEY_SERV)
    
    print(f'IMPORTANT: Press    -1  to exit the program when desired.\n\n')
    client_in = input(f'{input_id_client}{INPUT_STR}')
    while True:

        # pass client input into client ID var. + also get TGS ID
        if not check_send(conn, client_in) : break
        local_id_client = client_in
        local_id_auth = input(f'{input_id_auth}{INPUT_STR}')
        if not check_send(conn, local_id_auth) : break

        # send all contents after concat
        c_to_as_contents = concat(local_id_client, local_id_auth, ts())
        conn.send(str.encode(c_to_as_contents))

        # WAIT until AS is finished

        # update: instead of double en/de-cryption, do a verification 
        # check using the last part of 'resource' and the passed ticket.
        recv_data = conn.recv(RECV_BYTES)
        recv_data2 = conn.recv(RECV_BYTES)
        recv_as = descrypt(DEC, local_key_client, recv_data).decode()
        format_print(1, recv_as)
        
        # verify that the ticket is correct using comparison assertion
        assert split_as_to_c(recv_as, local_key_auth,
            local_key_client, local_id_client,
            TS_LEN, str(LIFETIME2)
        ) == repr(recv_data2), "Verification failed: ticket must match from original contents"
        
        #recv_ticket = descrypt(DEC, local_key_auth, recv_data2)
        # computer validates ticket, does user know the ticket?
        c_to_as_ticket_confirm = input(f"{ticket_c_as}{INPUT_STR}")
        c_to_as_key_confirm = input(f"{key_c_as}{INPUT_STR}")

        # now, for the client to service provider functionalities, concat and send
        local_id_serv = input(f'{input_id_serv}{INPUT_STR}')
        if not check_send(conn, client_in) : break
        new_authenticator = make_authenticator(local_key_client, local_id_client)
        c_to_v_contents = concat(local_id_serv, recv_data2, new_authenticator)
        conn.send(str.encode(c_to_v_contents))

        # WAIT until TGS is finished 

        recv_data = conn.recv(RECV_BYTES)
        #recv_tgs = descrypt(DEC, None, recv_data).decode()
            # change 'None' later

        check_send(conn, "-1")
        break       #end early hehe

    #client_socket.send(str.encode(EXIT_KEY))
        # skip for now
    print(f'{EXIT_KEY} pressed or process killed. Program is now finished.' )
    client_socket.close()
    sys.exit()

    # ...

# program for the authentication server
def auth_program():
    auth_socket = socket(AF_INET, SOCK_STREAM)
    auth_socket.connect((HOST, PORT)) 
    print(f"{temp}authentication server, connected to client...\n")

    while True:
        local_CLIENTkey = read_key(KEY_CLIENT)
        recv_data = auth_socket.recv(RECV_BYTES)
        from_client_to_as = recv_data.decode()
        if (from_client_to_as == str(EXIT_KEY)):
            print("Program closed using EXIT KEY. Bye!")
            auth_socket.close()
            sys.exit()
            
        format_print(0, from_client_to_as)
        get_contents = confirm_c_to_as(from_client_to_as)
        get_client_id = get_contents[0]
        get_tgs_id = get_contents[1]

        # generate key and ticket, then send in one overall message
        local_AUTHkey = read_key(KEY_AUTH)
        new_timestamp = ts()
        stream_c_as_key = stream_key()
        c_to_as_t = concat(stream_c_as_key, get_client_id, get_tgs_id,
            str(new_timestamp), str(LIFETIME2))
        c_to_as_ticket = descrypt(ENC, local_AUTHkey, c_to_as_t)
        c_to_as_feedback = concat(stream_c_as_key, get_tgs_id, str(new_timestamp),
            str(LIFETIME2), str(c_to_as_ticket))
        auth_socket.send(descrypt(ENC, local_CLIENTkey, c_to_as_feedback))
        auth_socket.send(c_to_as_ticket)

        # WAIT until client responds and sends another exchange with service provider ID
        recv_data = auth_socket.recv(RECV_BYTES)
        from_client_to_tgs = recv_data.decode()
        get_serv_id = split_c_to_v()

        # create ticket for service provider
        local_SERVkey = read_key(KEY_SERV)
        stream_c_v_key = stream_key()
        c_to_tgs_t = concat(stream_c_v_key, )

        # get diff. of current time and received time, 
        # and compare it to the lifetime of ticket

        # the TGS decrypts the ticket + authenticator, verifies
        # request; creates ticket for requested application server...

# program for the service provider
def serv_program():
    serv_socket = socket(AF_INET, SOCK_STREAM)
    serv_socket.connect((HOST, PORT))
    print(f"{temp}service provider, connected to client...\n")
    local_SERVkey = read_key(KEY_SERV)

    while True:
        recv_data = serv_socket.recv(RECV_BYTES)
        from_client = recv_data.decode()
        if (from_client == EXIT_KEY):
            break