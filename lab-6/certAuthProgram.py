from configurations import *

def certAuthProgram():
    print("Starting certificate authority program...")
    ca_socket = socket(AF_INET, SOCK_STREAM)
    ca_socket.connect((HOST, PORT))
    
    # send input
    ca_msg = input(INPUT_STR)
    
    while ca_msg.lower().strip() != EXIT_KEY:
        pass
    
    ca_socket.close()
    sys.exit()