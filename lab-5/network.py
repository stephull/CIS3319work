'''
    Network.py
    ::: Handles the socket program for client and server (TGS or auth. server) :::
'''
from configurations import *

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
        local_key_client = read_key(KEY_CLIENT)
        local_key_auth = read_key(KEY_AUTH)
        local_key_serv = read_key(KEY_SERV)
    
    print(f'IMPORTANT: Press    -1  to exit the program when desired.\n\n')
    while True:
        # pass client input into client ID var. + also get TGS ID
        client_in = input(f'{input_id_client}{INPUT_STR}')
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
        if valid_ticket and valid_key:
            print("\nTicket verification is valid")
        else : print("\nVerification is invalid. Restarting..."); break
    
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
        
        # confirm again for user to access service
        confirm_ticket_c_v = input(f'{ticket_c_v}{INPUT_STR}')
        if not check_send(conn, confirm_ticket_c_v) : break
        valid_ticket_c_v = (confirm_ticket_c_v == returned_tgs_ticket)
        confirm_key_c_v = input(f'{key_c_v}{INPUT_STR}')
        if not check_send(conn, confirm_key_c_v) : break
        valid_key_c_v = (confirm_key_c_v == local_key_client)
        if valid_ticket_c_v and valid_key_c_v:
            print("\nTicket verification is valid")  
        else : print("\nVerification is invalid. Restarting..."); break
        
        # (5th exchange) service provider
        ts5 = ts()
        new_authenticator2 = make_authenticator(recv_stream_key2, local_id_client, ts5)
        c_v_contents = concat(returned_tgs_ticket, new_authenticator2)
        conn.send(str.encode(c_v_contents))
        
        # finalize everything
        v_to_c = conn.recv(RECV_BYTES)
        print(f"\nService granted...\n({v_to_c})\n")
        break
    
    print(f'\n{EXIT_KEY} pressed or process killed. Program is now finished.\n' )
    client_socket.close()
    sys.exit()


'''
    Program for the authentication server
    Used for both the AS and the TGS (ticket-granting server)
'''
def server_program():
    auth_socket = socket(AF_INET, SOCK_STREAM)
    auth_socket.connect((HOST, PORT)) 
    print(f"{temp}authentication server, connected to client...\n")

    local_CLIENTkey = read_key(KEY_CLIENT)
    local_AUTHkey = read_key(KEY_AUTH)
    local_SERVkey = read_key(KEY_SERV)

    from_client_to_as = auth_socket.recv(RECV_BYTES).decode()
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
    print(f"\n{temp}SWITCHING TO SERVICE PROVIDER...\n")
    ts4 = ts()
    tgs_to_c_feedback = concat(stream_c_v_key, get_serv_id,
        str(ts4), str(c_to_tgs_ticket))       
    auth_socket.send(descrypt(ENC, stream_c_as_key, tgs_to_c_feedback))
    auth_socket.send(c_to_tgs_ticket)

    # going into the last (6th) exchange
    c_v_recv = auth_socket.recv(RECV_BYTES).decode()
    format_print(4, c_v_recv)
    index = KEY_LEN+len(ID_CLIENT)+len(ID_SERV)
    c_v_ts = c_v_recv[index:index+TS_LEN]
    auth_socket.send(descrypt(ENC, stream_c_v_key, str(int(c_v_ts)+1)))
    
    # finished 
    print("\nServer closing...\n")
    auth_socket.close()