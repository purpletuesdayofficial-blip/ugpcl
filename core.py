import os
import urllib.request

# ---------------- GLOBAL STATE ----------------

STATE = {}
COMMANDS = {}
DEBUG = False
CACHE_DIR = "./cache"


# ---------------- UTILITIES ----------------

def debug_log(msg):
    if DEBUG:
        print("[DEBUG]", msg)


def error(msg):
    raise Exception(msg)


# ---------------- PARSER ----------------

class Program:
    def __init__(self):
        self.schedule = []
        self.sections = {}


def parse(source):
    """
    Converts raw UGPCI source into structured program.
    """

    program = Program()

    # split lines, remove empty ones
    lines = [l.strip() for l in source.splitlines() if l.strip()]

    if not lines:
        error("Empty program")

    # first line = execution order
    program.schedule = lines[0].split("'")

    for raw in lines[1:]:
        # ---------------- COMMENTS ----------------

        # full-line comment
        if raw.startswith("$;"):
            continue

        # terminate program
        if raw == "!;":
            break

        # inline comment stripping
        raw = raw.split("$;")[0].strip()
        if not raw:
            continue

        # ---------------- SYNTAX PARSING ----------------

        if ":" not in raw:
            error(f"Invalid syntax (missing ':'): {raw}")

        left, right = raw.split(":", 1)

        if "," not in left:
            error(f"Invalid section format: {raw}")

        section, _ = left.split(",", 1)

        parts = right.split(",")

        program.sections.setdefault(section, []).append(parts)

        debug_log(f"Parsed: section={section}, instruction={parts}")

    return program


# ---------------- EXECUTION ENGINE ----------------

def run_program(program):
    """
    Executes parsed UGPCI program.
    """

    debug_log("Starting execution")

    # ---------------- SECTION 1 (CONFIG) ----------------
    for instr in program.sections.get("1", []):
        execute(instr)

    # ---------------- SCHEDULED SECTIONS ----------------
    for sec in program.schedule[1:]:
        for instr in program.sections.get(sec, []):
            execute(instr)


def execute(instr):
    """
    Executes a single instruction.
    """

    if not instr:
        return

    cmd = instr[0]

    debug_log(f"Executing: {instr}")

    # ---------------- SET ----------------
    if cmd == "set":
        _, key, value = instr
        STATE[key] = value
        return

    # ---------------- IMPORT ----------------
    if cmd == "import":
        import_module(instr[1])
        return

    # ---------------- PRINT ----------------
    if cmd == "print":
        typ = instr[1]
        val = instr[2]

        key = f"print:{typ}"

        if key in COMMANDS:
            COMMANDS[key](val)
        else:
            error(f"Unknown print type: {typ}")

        return

    # ---------------- DEBUG ----------------
    if cmd == "debug":
        global DEBUG
        DEBUG = True
        print("Debug mode enabled")
        return

    error(f"Unknown command: {cmd}")


# ---------------- MODULE SYSTEM (UGPIP) ----------------

def import_module(name):
    debug_log(f"Importing module: {name}")

    if name == "extra":
        load_extra()
        return

    if name == "graphic":
        load_graphic()
        return

    if name == "debug":
        load_debug()
        return

    if name.startswith("github:"):
        load_github(name)
        return

    error(f"Unknown module: {name}")


# ---------------- BUILTIN MODULES ----------------

def load_extra():
    COMMANDS["print:str"] = lambda v: print(v)
    COMMANDS["print:int"] = lambda v: print(int(v))


def load_graphic():
    def clear(_):
        print("\033[2J\033[H", end="")

    def colored(v):
        try:
            color, text = v.split("|")
        except:
            error("graphic.print,colored requires color|text")

        colors = {
            "red": "\033[31m",
            "green": "\033[32m",
            "blue": "\033[34m",
            "reset": "\033[0m"
        }

        print(colors.get(color, "") + text + colors["reset"])

    COMMANDS["clear:screen"] = clear
    COMMANDS["print:colored"] = colored


def load_debug():
    def dump(_):
        print("STATE DUMP:")
        for k, v in STATE.items():
            print(f"{k} = {v}")

    COMMANDS["dump:state"] = dump


# ---------------- GITHUB IMPORT (NO REQUESTS) ----------------

def load_github(path):
    path = path.replace("github:", "")
    user, repo, file = path.split("/")

    version = "main"
    if "@" in file:
        file, version = file.split("@")

    url = f"https://raw.githubusercontent.com/{user}/{repo}/{version}/{file}"

    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, path.replace("/", "_"))

    try:
        if os.path.exists(cache_file):
            source = open(cache_file).read()
        else:
            source = urllib.request.urlopen(url).read().decode()
            open(cache_file, "w").write(source)
    except Exception as e:
        error(f"GitHub module failed: {e}")

    parse_module(source)


def parse_module(source):
    """
    Minimal UGCM parser.
    """

    for line in source.splitlines():
        line = line.strip()

        if not line or line.startswith("module"):
            continue

        parts = line.split(",")

        if parts[0] == "command":
            # command,name,type
            _, name, typ = parts[:3]

            COMMANDS[f"{name}:{typ}"] = lambda v: print(v)


# ---------------- ENTRY POINT ----------------

def run_file(path):
    with open(path) as f:
        source = f.read()

    program = parse(source)
    run_program(program)