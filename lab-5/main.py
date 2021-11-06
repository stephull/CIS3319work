'''
    Main.py
    ::: Main executable program for lab, checks for correct arguments and limits :::
'''
from network import *

def main():
    assert len(sys.argv) == ARGS_LEN, "Number of arguments invalid"
    command = sys.argv[1]
    assert command == CLIENT or command == AUTH or command == SERV, "Commands must end with any of the following:\n'client', 'auth', 'serv'"
    assert int(PORT) in PORT_LIMITS, "Invalid port, check Configurations for validity of port connection"
    print(f'Using PORT number {PORT} to initiate program ({command})...')
    client_program() if command == CLIENT else serv_program() if command == SERV else auth_program()

if __name__ == "__main__":
    main()
