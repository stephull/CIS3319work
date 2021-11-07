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
check_ret = "Check in the Results folder for the key and ticket \n"

# does the input allow for program to continue running?
def check_send(conn, e):
    if str(e).lower().strip() != EXIT_KEY : return True
    conn.send(str.encode(EXIT_KEY))
    return False
def check_recv(conn, e):
    pass

# client program
def client_program():
    client_socket = socket(AF_INET, SOCK_STREAM)
    print(f'{temp}client. Waiting for servers to connect to program...\n')
    
    client_socket.bind((HOST, PORT))
    client_socket.listen(BACKLOG)
    conn, addr = client_socket.accept()

    if conn : print(f"Connected to TEST server\n(Address: {repr(addr).strip('()')})\n")
    print(f'IMPORTANT: Press    -1  to exit the program when desired.\n\n')
    client_in = input(f'{input_id_client}{INPUT_STR}')
    while True:
        # pass client input into client ID var. + also get TGS ID
        if not check_send(conn, client_in) : break
        local_id_client = client_in
        client_in = input(f'{input_id_auth}{INPUT_STR}')
        if not check_send(conn, client_in) : break
        local_id_auth = client_in

        # send all contents after concat
        c_to_as_contents = concat(local_id_client, local_id_auth, ts())
        conn.send(str.encode(c_to_as_contents))

        # same thing
        recv_data = conn.recv(RECV_BYTES)
        local_key_auth = read_key(KEY_AUTH)
        recv_auth = descrypt(DEC, local_key_auth, recv_data).decode()
        format_print(1, recv_auth)
        split_recv_auth = split_as_to_c(recv_auth, 
            local_key_auth, local_id_auth,
            TS_LEN, str(LIFETIME2))
        received_ticket = descrypt(DEC, local_key_auth, split_recv_auth)
        print("RECVTICKET TESTTTTTT: ", descrypt(DEC, local_key_auth, received_ticket))

        # now, for the client to service provider functionalities
        client_in = input(f'{input_id_serv}{INPUT_STR}')
        if not check_send(conn, client_in) : break

        # concat AND send messages
        #c_to_v_contents = concat(local_id_serv, )

        check_send(conn, "-1")
        break       #end early hehe

    #client_socket.send(str.encode(EXIT_KEY))
        # skip for now
    print(f'{EXIT_KEY} pressed or process killed. Program is now finished.' )
    client_socket.close()
    sys.exit()

    # once user logs on and gets service
    # user requests ticket-granting ticket ONCE (to AS)
    # send ID_c || ID_tgs || TS1 to server --> (1)

    # (2) --> once client gets key+ticket, client requests
    # service granting ticket (which the TGS handles)

    # ...

# program for the authentication server
def auth_program():
    auth_socket = socket(AF_INET, SOCK_STREAM)
    auth_socket.connect((HOST, PORT)) 
    print(f"{temp}authentication server, connected to client...\n")

    while True:
        recv_data = auth_socket.recv(RECV_BYTES)
        from_client = recv_data.decode()
        if (from_client == str(EXIT_KEY)):
            print("Program closed using EXIT KEY. Bye!")
            auth_socket.close()
            sys.exit()
            
        format_print(0, from_client)
        get_contents = confirm_c_to_as(from_client)
        get_client_id = get_contents[0]
        get_tgs_id = get_contents[1]

        # generate key and ticket, then send in one overall message
        local_AUTHkey = read_key(KEY_AUTH)
        new_timestamp = ts()
        c_to_as_ticket = local_AUTHkey + get_client_id + get_tgs_id + \
            str(new_timestamp) + str(LIFETIME2)
        c_to_as_ticket_des = str(descrypt(ENC, local_AUTHkey, c_to_as_ticket))
        c_to_as_feedback = local_AUTHkey + get_tgs_id + str(new_timestamp) \
            + str(LIFETIME2) + str(c_to_as_ticket_des)
        auth_socket.send(descrypt(ENC, local_AUTHkey, c_to_as_feedback))

    # the TGS decrypts the ticket+authenticator, verifies
    # request, then creates ticket for requested application server...

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