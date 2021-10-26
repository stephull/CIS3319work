'''
    Main.py
'''
from network import *

def main():
    assert len(sys.argv) is ARGS_LEN
    command = sys.argv[1]
    assert command is CLIENT or ASTGS or SERVPRO
    assert PORT < PORT_MAX and PORT >= PORT_MIN
    print(f'Using PORT number {PORT} to initiate program as {command}...')
    client_program() if command is CLIENT else server_program(ASTGS if command==ASTGS else SERVPRO)

if __name__ == "__main__":
    main()
