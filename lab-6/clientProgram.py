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
        assert c_socket.recv(RECV_BYTES).decode() == INTERMEDIATE_PASS, "Error: invalid connection for client-server exchange.\n"
        c_socket.send(str(JUNK).encode())
        
        # SEND third exchange: C -> S
        # >> ID(s) || TS3
        c_s_1_ts = str(ts())
        c_s_1_concat = concat(ID_S, c_s_1_ts)
        c_socket.send(str.encode(c_s_1_concat))
        
        # PRINTOUT 3
        print(PO[2][0])
        print(ID_S, c_s_1_ts, '\n\n')
        
        # RECV fourth exchange: S -> C
        # >> PK(s) || Cert(s) || TS4
        s_c_recv = c_socket.recv(RECV_BYTES).decode()
        s_pub_key, cert, returned_ts = s_c_1_split(s_c_recv)
        
        # PRINTOUT 4
        print(PO[2][1])
        print(s_pub_key, cert, returned_ts, '\n\n')
        
        # SEND fifth exchange: C -> S
        # >> RSA(PKs) [K(tmp2) || ID(c) || IP(c) || Port(c) || TS5], generate K(tmp2) on C
        
        # before we move on, we must verify S's public key and certificate
        
        ktmp2 = stream_key()
        c_s_2_ts = str(ts())
        c_s_2_concat = concat(ktmp2, ID_C, HOST, str(PORT), c_s_2_ts)
        c_s_2_digits = digitize_text(ENC, c_s_2_concat)
        s5_send = rsacrypt(c_s_2_digits)
        c_socket.send(str(s5_send).encode())
        
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