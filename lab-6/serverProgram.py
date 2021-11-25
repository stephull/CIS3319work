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
        if conn:
            priv_s_rsa_key = begin_rsa()
            # Note that this is only required for RSA stuff, not mentioned in lab protocol
            #, "\n\nERROR: RSA private key formulation is broken, sorry. Try again!\n"
            print("\nUPDATE: Connected to client...\n")
        
        # SEND first exchange: S -> CA
        # >> RSA(PKca) [K(tmp1) || ID(s) || TS1], K(tmp1) generates on S
        local_key_temp1 = stream_key()
        exchange1_contents = concat(local_key_temp1, ID_S, str(ts()))
        exchange1_digits = digitize_text(ENC, exchange1_contents)
        
        pub_rsa_key = read_key(RSA_PUB_KEY, True)   # returns n and e, respectively
        s1_send_msg = rsacrypt(ENC, pub_rsa_key[0], pub_rsa_key[1], exchange1_digits)   # P^e mod n --> C
                
        # https://www.geeksforgeeks.org/python-interconvert-tuple-to-byte-integer/
        conn.send(str(priv_s_rsa_key[0]).encode())
        conn.send(str(priv_s_rsa_key[1]).encode())
        conn.recv(RECV_BYTES)
        conn.send(str(s1_send_msg).encode())
        conn.send(str(exchange1_contents).encode())
        
        # RECV second exchange: CA -> S
        
        # RECV third exchange: C -> S
        
        # SEND fourth exchange: S -> C
        # >> PK(s) || Cert(s) || TS4
        
        # RECV fifth exchange: C -> S
        
        # SEND sixth exchange: S -> C
        # >> DES(Ktmp2) [K(sess) || LT(sess) || ID(c) || TS6]
        
        # RECV seventh exchange: C -> S
        
        # SEND eighth exchange: S -> C
        # >> DES(Ksess) [data || TS8]
        
        # fin 
        # https://www.positronx.io/create-socket-server-with-multiple-clients-in-python/
        
        break
    
    s_socket.close()
    sys.exit()