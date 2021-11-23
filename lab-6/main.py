'''
    Main.py : main executable for project
'''

from configurations import *
from clientProgram import *
from serverProgram import *
from certAuthProgram import *

def main():
    assert PORT in PORT_LIM, "Port number must be within range."
    assert len(sys.argv) == ARGS_LEN, f"Argument length must be {ARGS_LEN} arguments long, after python3."
    comm = sys.argv[1]
    assert comm==CLIENT or comm==SERVER or comm==CA, f"Must pick the following options: \n{CLIENT}\n{CA}\n{SERVER}"
    clientProgram() if comm == CLIENT else certAuthProgram() if comm == CA else serverProgram()

if __name__ == "__main__":
    main()