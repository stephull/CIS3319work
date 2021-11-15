'''
    Client program
'''

from configurations import *

def clientProgram():
    print("Starting client program...")
    c_socket = socket(AF_INET, SOCK_STREAM)
    c_socket.connect((HOST, PORT))
    
    # TEST
    rsacrypt(ENC, 0, 0)
    
    # send input
    c_msg = input(INPUT_STR)
    
    while c_msg.lower().strip() != EXIT_KEY:
        # maybe change above???
        
        # send contents
        pass
    
    c_socket.close()
    sys.exit()