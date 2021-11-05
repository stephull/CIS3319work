'''
    Network.py
    ::: Handles the socket program for client and server (TGS or auth. server) :::
'''
from configurations import *

# start, for each program
temp = "\n>>> Log:    Start "

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

    # once user logs on and gets service
    # user requests ticket-granting ticket ONCE (to AS)
    # send ID_c || ID_tgs || TS1 to server --> (1)

    # (2) --> once client gets key+ticket, client requests
    # service granting ticket (which the TGS handles)

    # ...

# program for the authentication server
def auth_program():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((HOST, PORT)) 
    print(f"{temp}authentication server, connected to client...\n")
    local_AUTHkey = read_key(KEY_AUTH)

    # (1) --> AS party must verify user's access right and create
    # the ticket + session key. Results are encrypted, using key
    # derived from user's timestamp

    # send the key and ticket to the client --> (2)

    # (3) --> the TGS decrypts the ticket+authenticator, verifies
    # request, then creates ticket for requested application server...

# program for the service provider
def serv_program():
    serv_socket = socket(AF_INET, SOCK_STREAM)
    serv_socket.connect((HOST, PORT))
    print(f"{temp}service provider, connected to client...\n")
    local_SERVkey = read_key(KEY_SERV)