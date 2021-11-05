'''
    Main.py
    ::: Main executable program for lab, checks for correct arguments and limits :::
'''
from network import *

def main():
    assert len(sys.argv) == ARGS_LEN
    command = sys.argv[1]
    assert command == CLIENT or command == AUTH or command == SERV
    assert int(PORT) in PORT_LIMITS
    print(f'Using PORT number {PORT} to initiate program ({command})...')
    client_program() if command == CLIENT else serv_program() if command == SERV else auth_program()

if __name__ == "__main__":
    main()
