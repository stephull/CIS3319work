'''
    Server program: for server
'''

from configurations import *
from rsa_functions import *

def serverProgram():
    print("Starting server program...")
    s_socket = socket(AF_INET, SOCK_STREAM)
    s_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s_socket.bind((HOST, PORT))
    s_socket.listen(BACKLOG)
    
    while True:
        conn, addr = s_socket.accept()
        if conn:    print("\nUPDATE: Connected to client...\n")
        
        # SEND first exchange: S -> CA
        # >> RSA(PKca) [K(tmp1) || ID(s) || TS1], K(tmp1) generates on S
        
        # RECV second exchange: CA -> S
        # >> DES(Ktmp1) [PK(s) || SK(s) || Cert(s)|| ID(s) || TS2]
        # >> >> Cert(s) = Sign(SKca) [ID(s) || ID(ca) || PK(s)]
        # >> >> Sign(SKca) is RSA signature generation with specified private key
        
        # RECV third exchange: C -> S
        # >> ID(s) || TS3
        
        # SEND fourth exchange: S -> C
        # >> PK(s) || Cert(s) || TS4
        
        # RECV fifth exchange: C -> S
        # >> RSA(PKs) [K(tmp2) || ID(c) || IP(c) || Port(c) || TS5], generate K(tmp2) on C
        
        # SEND sixth exchange: S -> C
        # >> DES(Ktmp2) [K(sess) || LT(sess) || ID(c) || TS6]
        
        # RECV seventh exchange: C -> S
        # >> DES(Ksess) [req || TS7]
        
        # SEND eighth exchange: S -> C
        # >> DES(Ksess) [data || TS8]
        
        # fin 
        # https://www.positronx.io/create-socket-server-with-multiple-clients-in-python/
        
        break
    
    s_socket.close()
    sys.exit()