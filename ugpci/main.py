import sys
from parser import parse
from executor import Executor

def main():
    if len(sys.argv) < 2:
        print("Usage: ugpci file.ugcpl")
        return

    with open(sys.argv[1], "r") as f:
        source = f.read()

    program = parse(source)
    Executor(program).run()

if __name__ == "__main__":
    main()
