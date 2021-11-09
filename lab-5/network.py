'''
    Network.py
    ::: Handles the socket program for client and server (TGS or auth. server) :::
'''
from configurations import *

temp = "\n>>> Log:    Start "
input_id_client = "Enter the client ID: \n"
input_id_auth = "Enter the TGS access ID (for auth. server): \n"
input_id_serv = "Enter the service provider ID: \n"
ticket_c_as = "Confirm ticket to proceed to TGS: \n"
key_c_as = "Enter key given to proceed to TGS: \n"
ticket_c_v = "Confirm ticket to proceed to service provider: \n"
key_c_v = "Enter key given to proceed to service provider: \n"


'''
    Main, client program; used to begin execution
'''
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

        # send all contents after concat (1st exchange)
        c_to_as_contents = concat(local_id_client, local_id_auth, ts())
        conn.send(str.encode(c_to_as_contents))

        # WAIT until AS is finished

        # update: instead of double en/de-cryption, do a verification 
        # check using the last part of 'resource' and the passed ticket.
        recv_data = conn.recv(RECV_BYTES)
        recv_data2 = conn.recv(RECV_BYTES)
        recv_as = descrypt(DEC, local_key_client, recv_data).decode()
        recv_ticket = descrypt(DEC, local_key_auth, recv_data2).decode()
        recv_stream_key1 = str(recv_as[:KEY_LEN])
        format_print(1, recv_as)
        
        # verify that the ticket is correct using comparison assertion
        # and user must do the same via input
        confirm_ticket_c_as = input(f'{ticket_c_as}{INPUT_STR}')
        if not check_send(conn, confirm_ticket_c_as) : break
        valid_ticket = (recv_ticket == confirm_ticket_c_as)  
        confirm_key_c_as = input(f'{key_c_as}{INPUT_STR}')
        if not check_send(conn, confirm_key_c_as) : break
        valid_key = (local_key_client == confirm_key_c_as)
        print("\nTicket verification is valid" if valid_ticket and valid_key else "\nVerification is invalid")
    
        # now, for the client to service provider functionalities, concat and send
        local_id_serv = input(f'{input_id_serv}{INPUT_STR}')
        if not check_send(conn, local_id_serv) : break
        ts3 = ts()
        new_authenticator1 = make_authenticator(recv_stream_key1, local_id_client, ts3)
            # new timestamp is created within authenticator creation
            
        # (3rd exchange)
        c_to_as_contents = concat(local_id_serv, recv_data2, new_authenticator1)
        conn.send(str.encode(c_to_as_contents))
        conn.send(str.encode("Ticket validity: " + str(valid_ticket)))

        # WAIT until TGS is finished 

        recv_tgs = conn.recv(RECV_BYTES)
        recv_tgs_ticket = conn.recv(RECV_BYTES)
        returned_tgs = descrypt(DEC, recv_stream_key1, recv_tgs).decode()
        returned_tgs_ticket = descrypt(DEC, local_key_serv, recv_tgs_ticket)
        returned_tgs_ticket = returned_tgs_ticket.decode()
        recv_stream_key2 = str(returned_tgs[:KEY_LEN])
        format_print(3, returned_tgs)
        
        # (5th exchange)
        # IMPORTANT: at this point, we need to send the following in a new system
        # (service provider)
        ts5 = ts()
        new_authenticator2 = make_authenticator(recv_stream_key2, local_id_client, ts5)
        c_v_contents = concat(returned_tgs_ticket, new_authenticator2)
        conn.send(str.encode(c_v_contents))

    print(f'{EXIT_KEY} pressed or process killed. Program is now finished.' )
    client_socket.close()
    sys.exit()


'''
    Program for the authentication server
    Used for both the AS and the TGS (ticket-granting server)
'''
def auth_program():
    auth_socket = socket(AF_INET, SOCK_STREAM)
    auth_socket.connect((HOST, PORT)) 
    print(f"{temp}authentication server, connected to client...\n")

    local_CLIENTkey = read_key(KEY_CLIENT)
    local_AUTHkey = read_key(KEY_AUTH)
    local_SERVkey = read_key(KEY_SERV)

    from_client_to_as = auth_socket.recv(RECV_BYTES).decode()
    if (from_client_to_as == str(EXIT_KEY)):
        print("Program closed using EXIT KEY. Bye!")
        auth_socket.close()
        sys.exit()
        
    format_print(0, from_client_to_as)
    get_contents = confirm_c_to_as(from_client_to_as)
    get_client_id = get_contents[0]
    get_tgs_id = get_contents[1]

    # generate key and ticket, then send in one overall message
    new_timestamp = ts()
    stream_c_as_key = stream_key()
    c_to_as_t = concat(stream_c_as_key, get_client_id, get_tgs_id,
        str(new_timestamp), str(LIFETIME2))
    c_to_as_ticket = descrypt(ENC, local_AUTHkey, c_to_as_t)
    c_to_as_feedback = concat(stream_c_as_key, get_tgs_id, str(new_timestamp),
        str(LIFETIME2), str(c_to_as_ticket))
    
    # before sending, we also should place the ticket and key in a Results file
    # and let user know of transition from AS to TGS
    # (2nd exchange)
    write_to_results(RET_1, c_to_as_t, local_CLIENTkey)
    print(f"\n{temp}SWITCHING TO TGS...\n")
    auth_socket.send(descrypt(ENC, local_CLIENTkey, c_to_as_feedback))
    auth_socket.send(c_to_as_ticket)

    # WAIT until client responds and sends another exchange with service provider ID
    from_client_to_tgs = auth_socket.recv(RECV_BYTES).decode()
    ticket_valid = auth_socket.recv(RECV_BYTES).decode()        
    format_print(2, from_client_to_tgs, '\n', ticket_valid)
    
    get_serv_id = split_c_to_v(from_client_to_tgs)
    assert get_serv_id.strip() == ID_SERV, "\nService provider ID is not valid, try again."

    # create ticket for service provider (4th exchange)
    stream_c_v_key = stream_key()
    ts3 = ts()
    c_to_tgs_t = concat(stream_c_v_key, get_client_id,
        get_serv_id, str(ts3), str(LIFETIME4))
    c_to_tgs_ticket = descrypt(ENC, local_SERVkey, c_to_tgs_t)
    write_to_results(RET_2, c_to_tgs_t, local_CLIENTkey)

    ts4 = ts()
    tgs_to_c_feedback = concat(stream_c_v_key, get_serv_id,
        str(ts4), str(c_to_tgs_ticket))       
    auth_socket.send(descrypt(ENC, stream_c_as_key, tgs_to_c_feedback))
    auth_socket.send(c_to_tgs_ticket)
    
    # test 6th exchange (not supposed to be here tho)
    print("Authentication server closing. Please redirect to the service provider...")
    auth_socket.close()

'''
    Program for service provider
'''
def serv_program():
    serv_socket = socket(AF_INET, SOCK_STREAM)
    serv_socket.connect((HOST, PORT))
    print(f"{temp}service provider, connected to client...\n")
    local_SERVkey = read_key(KEY_SERV)

    recv_data = serv_socket.recv(RECV_BYTES)
    from_client = recv_data.decode()
    
    serv_socket.close()