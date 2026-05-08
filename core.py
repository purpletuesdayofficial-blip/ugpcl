import os
import requests

STATE = {}
COMMANDS = {}

CACHE = "./cache"


# ---------------- PARSER ----------------

def parse(source):
    lines = [l.strip() for l in source.splitlines() if l.strip()]

    schedule = lines[0].split("'")
    sections = {}

    for line in lines[1:]:
        if line == "!;":
            break

        left, right = line.split(":", 1)
        sec, _ = left.split(",")

        sections.setdefault(sec, []).append(right.split(","))

    return schedule, sections


# ---------------- EXECUTION ----------------

def execute_instruction(i):
    cmd = i[0]

    if cmd == "set":
        STATE[i[1]] = i[2]

    elif cmd == "import":
        import_module(i[1])

    elif cmd == "print":
        typ = i[1]
        val = i[2]
        COMMANDS.get(f"print:{typ}", print)(val)


def run(schedule, sections):
    for instr in sections.get("1", []):
        execute_instruction(instr)

    for sec in schedule[1:]:
        for instr in sections.get(sec, []):
            execute_instruction(instr)


# ---------------- MODULE SYSTEM ----------------

def import_module(name):
    if name == "extra":
        load_extra()
    elif name == "graphic":
        load_graphic()
    elif name == "debug":
        load_debug()
    elif name.startswith("github:"):
        load_github(name)


# ---------------- EXTRA MODULE ----------------

def load_extra():
    COMMANDS["print:str"] = lambda v: print(v)
    COMMANDS["print:int"] = lambda v: print(int(v))


# ---------------- GRAPHIC MODULE ----------------

def load_graphic():
    def clear(_):
        print("\033[2J\033[H", end="")

    def color(v):
        c, t = v.split("|")
        colors = {
            "red": "\033[31m",
            "green": "\033[32m",
            "blue": "\033[34m",
            "reset": "\033[0m"
        }
        print(colors.get(c, "") + t + colors["reset"])

    COMMANDS["clear:screen"] = clear
    COMMANDS["print:colored"] = color


# ---------------- DEBUG MODULE ----------------

def load_debug():
    def dump(_):
        print("STATE:", STATE)

    COMMANDS["dump:state"] = dump


# ---------------- GITHUB IMPORT ----------------

def load_github(path):
    path = path.replace("github:", "")
    user, repo, file = path.split("/")

    version = "main"
    if "@" in file:
        file, version = file.split("@")

    url = f"https://raw.githubusercontent.com/{user}/{repo}/{version}/{file}"

    os.makedirs(CACHE, exist_ok=True)
    cache_file = os.path.join(CACHE, path.replace("/", "_"))

    if os.path.exists(cache_file):
        source = open(cache_file).read()
    else:
        source = requests.get(url).text
        open(cache_file, "w").write(source)

    parse_module(source)


def parse_module(source):
    for line in source.splitlines():
        line = line.strip()
        if not line or line.startswith("module"):
            continue

        parts = line.split(",")

        if parts[0] == "command":
            _, name, typ = parts[:3]

            COMMANDS[f"{name}:{typ}"] = lambda v: print(v)


# ---------------- RUN FILE ----------------

def run_file(path):
    with open(path) as f:
        source = f.read()

    schedule, sections = parse(source)
    run(schedule, sections)
