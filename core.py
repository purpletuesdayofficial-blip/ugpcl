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
    program = Program()

    lines = [l.strip() for l in source.splitlines() if l.strip()]

    if not lines:
        error("Empty program")

    # execution order
    program.schedule = lines[0].split("'")

    for raw in lines[1:]:
        # full line comment
        if raw.startswith("$;"):
            continue

        if raw == "!;":
            break

        # inline comments
        raw = raw.split("$;")[0].strip()
        if not raw:
            continue

        if ":" not in raw:
            error(f"Invalid syntax: {raw}")

        left, right = raw.split(":", 1)

        if "," not in left:
            error(f"Invalid section format: {raw}")

        section, _ = left.split(",", 1)

        parts = right.split(",")

        program.sections.setdefault(section, []).append(parts)

        debug_log(f"Parsed {section}: {parts}")

    return program


# ---------------- EXECUTION ----------------

def run_program(program):
    debug_log("Running program")

    # config section always first
    for instr in program.sections.get("1", []):
        execute(instr)

    # scheduled execution
    for sec in program.schedule[1:]:
        for instr in program.sections.get(sec, []):
            execute(instr)


def execute(instr):
    if not instr:
        return

    cmd = instr[0]
    args = instr[1:]

    debug_log(f"EXEC: {instr}")

    # ---------------- SET ----------------
    if cmd == "set":
        if len(args) < 2:
            error("set requires key,value")
        STATE[args[0]] = args[1]
        return

    # ---------------- IMPORT ----------------
    if cmd == "import":
        import_module(args[0])
        return

    # ---------------- DEBUG TOGGLE ----------------
    if cmd == "debug":
        global DEBUG
        DEBUG = True
        print("Debug enabled")
        return

    # ---------------- COMMAND DISPATCH (FIXED) ----------------
    # supports:
    # clear,screen → clear:screen
    # print,colored → print:colored

    if len(args) > 0:
        key = f"{cmd}:{args[0]}"
        payload = args[1:] if len(args) > 1 else []

        if key in COMMANDS:
            COMMANDS[key]("|".join(payload) if payload else "")
            return

    # fallback: raw command
    if cmd in COMMANDS:
        COMMANDS[cmd]("|".join(args) if args else "")
        return

    error(f"Unknown command: {cmd}")


# ---------------- MODULE SYSTEM ----------------

def import_module(name):
    debug_log(f"Import: {name}")

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


# ---------------- MODULE: EXTRA ----------------

def load_extra():
    COMMANDS["print:str"] = lambda v: print(v)
    COMMANDS["print:int"] = lambda v: print(int(v))


# ---------------- MODULE: GRAPHIC ----------------

def load_graphic():

    def clear(_):
        print("\033[2J\033[H", end="")

    def colored(v):
        try:
            color, text = v.split("|")
        except:
            error("format: print,colored,color|text")

        colors = {
            "red": "\033[31m",
            "green": "\033[32m",
            "blue": "\033[34m",
            "reset": "\033[0m"
        }

        print(colors.get(color, "") + text + colors["reset"])

    COMMANDS["clear:screen"] = clear
    COMMANDS["print:colored"] = colored


# ---------------- MODULE: DEBUG ----------------

def load_debug():

    def dump(_):
        print("STATE:")
        for k, v in STATE.items():
            print(f"{k} = {v}")

    COMMANDS["dump:state"] = dump


# ---------------- GITHUB MODULE LOADER ----------------

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
        error(f"GitHub import failed: {e}")

    parse_module(source)


def parse_module(source):
    for line in source.splitlines():
        line = line.strip()

        if not line or line.startswith("module"):
            continue

        parts = line.split(",")

        if parts[0] == "command":
            # command,name,type
            _, name, typ = parts[:3]

            # FIXED mapping
            COMMANDS[f"{name}:{typ}"] = lambda v: print(v)


# ---------------- RUN FILE ----------------

def run_file(path):
    with open(path) as f:
        source = f.read()

    program = parse(source)
    run_program(program)