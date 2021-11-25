'''
    Server program: for server
'''

from configurations import *
from rsa_functions import *

# for any exchange between the server and certificate authenticator
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
        global ca_s_pub_key, cert       # for future exchanges with client...
        ca_s_pub_key, ca_s_priv_key, cert = ca_s_split(returned_des_contents)
        
        # PRINTOUT 2
        print(PO[1][1])
        print(returned_des_key)
        print([ca_s_pub_key, ca_s_priv_key])
        print(cert, '\n\n')
        
        # Exit out of first-half of server, continue to serverProgram2 for rest of lab (client-server exchange).
        print("To continue the lab, open new terminal and type in the following:\n")
        print(f"\tpython3 main.py {CLIENT}")
        break
    
    s_socket.close()
    serverProgram2()
    
# for any communication between server and client
def serverProgram2():
    time.sleep(1)
    s_socket = socket(AF_INET, SOCK_STREAM)
    s_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s_socket.bind((HOST, PORT))
    s_socket.listen(BACKLOG)
    
    while True:
        conn, addr = s_socket.accept()
        if conn : conn.send(str(INTERMEDIATE_PASS).encode())
        if (conn.recv(RECV_BYTES).decode() != JUNK): continue   # don't go anywhere until valid connection is made
    
        # RECV third exchange: C -> S
        recv_c_s_1 = conn.recv(RECV_BYTES).decode()
        returned_s_id, returned_c_s_1_ts = c_s_1_split(recv_c_s_1)
        print(returned_s_id, returned_c_s_1_ts)
        
        # PRINTOUT 3
        print(PO[2][0])
        print(returned_s_id, returned_c_s_1_ts, '\n\n')
    
        # SEND fourth exchange: S -> C
        # >> PK(s) || Cert(s) || TS4
        s_c_1_ts = str(ts())
        s_c_1_concat = concat(ca_s_pub_key, cert, s_c_1_ts)
        conn.send(str(s_c_1_concat).encode())
        
        # PRINTOUT 4
        print(PO[2][1])
        print(ca_s_pub_key, cert, s_c_1_ts, '\n\n')
        
        # RECV fifth exchange: C -> S
        
        
        # SEND sixth exchange: S -> C
        # >> DES(Ktmp2) [K(sess) || LT(sess) || ID(c) || TS6]
        
        # RECV seventh exchange: C -> S
        
        # SEND eighth exchange: S -> C
        # >> DES(Ksess) [data || TS8]
        
        # EXTRA: https://www.positronx.io/create-socket-server-with-multiple-clients-in-python/
        break
        
    # Exiting out of everything.
    print("\nTerminating lab...\n\n")
    s_socket.close()
    sys.exit()