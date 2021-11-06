'''
    Network.py
    ::: Handles the socket program for client and server (TGS or auth. server) :::
'''
from configurations import *

# instructions for every program
temp = "\n>>> Log:    Start "
input_id_client = "Enter the client ID: \n"
input_id_auth = "Enter the TGS access ID (for auth. server): \n"
check_ret = "Check in the Results folder for the key and ticket \n"

# important function to determine validity of input
# i.e. does the input allow for program to continue running?
def exit_cond(e) : return str(e).lower().strip() != EXIT_KEY
def pass_input(conn, e):
    if not exit_cond(e):
        conn.send(str.encode(EXIT_KEY))
        return False
    return True

# client program
def client_program():
    client_socket = socket(AF_INET, SOCK_STREAM)
    print(f'{temp}client. Waiting for servers to connect to program...\n')
    
    client_socket.bind((HOST, PORT))
    client_socket.listen(BACKLOG)
    conn, addr = client_socket.accept()

    if conn:
        local_CLIENTkey = read_key(KEY_CLIENT)
        print(f"Connected to TEST server\n(Address: {repr(addr).strip('()')})\n")

    print(f'IMPORTANT: Press    -1  to exit the program when desired.\n\n')
    client_in = input(f'{input_id_client}{INPUT_STR}')
    while True:
        # pass client input into client ID var. + also get TGS ID
        if not pass_input(conn, client_in) : break
        local_id_client = client_in
        client_in = input(f'{input_id_auth}{INPUT_STR}')
        if not pass_input(conn, client_in) : break
        local_id_auth = client_in

        # send all contents after concat
        c_to_as_contents = concat(local_id_client, local_id_auth, ts())
        conn.send(str.encode(c_to_as_contents))

        # same thing
        recv_data = conn.recv(RECV_BYTES)
        respond_client = recv_data.decode()
        # ::::::::::: not working code, yet

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
    local_AUTHkey = read_key(KEY_AUTH)

    while True:
        recv_data = auth_socket.recv(RECV_BYTES)
        from_client = recv_data.decode()
        if (from_client == str(EXIT_KEY)):
            print("Program closed using EXIT KEY. Bye!")
            auth_socket.close()
            sys.exit()
        else:
            get_contents = confirm_c_to_as(from_client.strip())
            print("Cool: ",get_contents)

    # (1) --> AS party must verify user's access right and create
    # the ticket + session key. Results are encrypted, using key
    # derived from user's timestamp

    # send the key and ticket to the client --> (2)

    # (3) --> the TGS decrypts the ticket+authenticator, verifies
    # request, then creates ticket for requested application server...

# program for the service provider
'''
    Todo: WORK ON THIS LATER!!!
'''
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