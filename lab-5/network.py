'''
    Network.py
'''
from configurations import *

# socket used for whichever program is declared in main
soc = socket(AF_INET, SOCK_STREAM)

# client program
def client_program():
    soc.bind((LOCALHOST, PORT))
    soc.listen(BACKLOG)
    conn, addr = soc.accept()

    # once user logs on and gets service
    # user requests ticket-granting ticket ONCE (to AS)
    # send ID_c || ID_tgs || TS1 to server --> (1)

    # (2) --> once client gets key+ticket, client requests
    # service granting ticket (which the TGS handles)

    # ...

# program for the authentication server AND/OR service provider
def server_program(party):
    assert party is ASTGS or SERVPRO
    soc.connect((LOCALHOST, PORT)) 

    # (1) --> AS party must verify user's access right and create
    # the ticket + session key. Results are encrypted, using key
    # derived from user's timestamp

    # send the key and ticket to the client --> (2)

    # (3) --> the TGS decrypts the ticket+authenticator, verifies
    # request, then creates ticket for requested application server...

