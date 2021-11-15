'''
    Server program: for server
'''

from configurations import *

def serverProgram():
    print("Starting server program...")
    s_socket = socket(AF_INET, SOCK_STREAM)
    s_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s_socket.bind((HOST, PORT))
    s_socket.listen(BACKLOG)
    
    while True:
        conn, addr = s_socket.accept()
        if conn:    print("\nUPDATE: Connected to client...\n")
        
        
        # https://www.positronx.io/create-socket-server-with-multiple-clients-in-python/
    
    s_socket.close()
    sys.exit()