'''
    Client program
'''

from configurations import *
from rsa_functions import *

def clientProgram():
    print("Starting client program...")
    c_socket = socket(AF_INET, SOCK_STREAM)
    c_socket.connect((HOST, PORT))

    while True:
        print("\nConnected to client program...\n")
        
        # SEND third exchange: C -> S
        # >> ID(s) || TS3
        c_s_1_concat = concat(ID_S, str(ts()))
        c_socket.send(str.encode(c_s_1_concat))
        
        # RECV fourth exchange: S -> C
        # >> PK(s) || Cert(s) || TS4
        s_c_recv = c_socket.recv(RECV_BYTES).decode()
        s_pub_key, cert, returned_ts = s_c_split(s_c_recv)
        
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