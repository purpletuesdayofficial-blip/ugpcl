import sys
from core import run_file

if len(sys.argv) < 2:
    print("Usage: ugpci file.ugcpl")
    exit()

run_file(sys.argv[1])
