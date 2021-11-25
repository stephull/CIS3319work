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
            print("\nUPDATE: Connected to client...\n")
            conn.send(JUNK.encode())
            pub_rsa_key = eval(conn.recv(RECV_BYTES).decode())
        
        # SEND first exchange: S -> CA
        # >> RSA(PKca) [K(tmp1) || ID(s) || TS1], K(tmp1) generates on S
        local_key_temp1 = stream_key()
        exchange1_contents = concat(local_key_temp1, ID_S, str(ts()))
        exchange1_digits = digitize_text(ENC, exchange1_contents)
        s1_send_msg = rsacrypt(pub_rsa_key[0], pub_rsa_key[1], exchange1_digits)   # P^e mod n --> C
                
        # https://www.geeksforgeeks.org/python-interconvert-tuple-to-byte-integer/
        conn.send(str(s1_send_msg).encode())    # main
        conn.recv(RECV_BYTES)
        conn.send(str(exchange1_contents).encode())
        
        # PRINTOUT 1
        print(PO[0][0])
        print(s1_send_msg)
        print(local_key_temp1, '\n\n')
        
        # RECV second exchange: CA -> S
        returned_des_key = conn.recv(RECV_BYTES)
        returned_des_contents = descrypt(DEC, local_key_temp1, returned_des_key).decode()
        ca_s_pub_key, ca_s_priv_key, cert = ca_s_split(returned_des_contents)
        
        # PRINTOUT 2
        print(PO[1][1])
        print(returned_des_key)
        print([ca_s_pub_key, ca_s_priv_key])
        print(cert, '\n\n')
        
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