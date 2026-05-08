import os
import requests

COMMANDS = {}
CACHE = "./cache"


# ---------------- PARSER ----------------

class Program:
    def __init__(self):
        self.schedule = []
        self.sections = {}


def parse(source):
    p = Program()

    lines = [l.strip() for l in source.splitlines() if l.strip()]

    p.schedule = lines[0].split("'")

    for line in lines[1:]:
        if line == "!;":
            break

        left, right = line.split(":", 1)
        sec, _ = left.split(",")

        p.sections.setdefault(sec, []).append(right.split(","))

    return p


# ---------------- RUNTIME ----------------

def run_program(p):
    for instr in p.sections.get("1", []):
        execute(instr)

    for sec in p.schedule[1:]:
        for instr in p.sections.get(sec, []):
            execute(instr)


# ---------------- EXECUTOR ----------------

def execute(i):
    cmd = i[0]

    if cmd == "set":
        return

    if cmd == "import":
        import_module(i[1])

    if cmd == "print":
        typ, val = i[1], i[2]
        COMMANDS.get(f"print:{typ}", print)(val)


# ---------------- UGPIP ----------------

def import_module(name):
    if name == "extra":
        load_extra()
        return

    if name == "graphic":
        load_graphic()
        return

    if name.startswith("github:"):
        load_github(name)


# ---------------- MODULES ----------------

def load_extra():
    COMMANDS["print:str"] = print
    COMMANDS["print:int"] = lambda v: print(int(v))


def load_graphic():
    print("\033[2J\033[H", end="")

    def colored(v):
        c, t = v.split("|")
        colors = {
            "red": "\033[31m",
            "green": "\033[32m",
            "blue": "\033[34m",
            "reset": "\033[0m"
        }
        print(colors.get(c, "") + t + colors["reset"])

    COMMANDS["print:colored"] = colored


# ---------------- FILE RUNNER ----------------

def run_file(path):
    with open(path) as f:
        source = f.read()

    program = parse(source)
    run_program(program)
