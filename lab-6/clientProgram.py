'''
    Client program
'''

from configurations import *
from rsa_functions import *

def clientProgram():
    print("Starting client program...")
    c_socket = socket(AF_INET, SOCK_STREAM)
    c_socket.connect((HOST, PORT))
    
    # TEST for rsa
    rsacrypt(ENC, 0, 0)
    
    # send input
    c_msg = input(INPUT_STR)
    
    while c_msg.lower().strip() != EXIT_KEY:    # maybe change above???
        
        # SEND third exchange: C -> S
        # >> ID(s) || TS3
        
        # RECV fourth exchange: S -> C
        # >> PK(s) || Cert(s) || TS4
        
        # SEND fifth exchange: C -> S
        # >> RSA(PKs) [K(tmp2) || ID(c) || IP(c) || Port(c) || TS5], generate K(tmp2) on C
        
        # RECV sixth exchange: S -> C
        # >> DES(Ktmp2) [K(sess) || LT(sess) || ID(c) || TS6]
        
        # SEND seventh exchange: C -> S
        # >> DES(Ksess) [req || TS7]
        
        # RECV eighth exchange: S -> C
        # >> DES(Ksess) [data || TS8]
        
        # fin 
        break
    
    c_socket.close()
    sys.exit()