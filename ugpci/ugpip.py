import os
import requests

COMMANDS = {}

CACHE_DIR = "./cache"


def load_extra():
    def print_str(v):
        print(v)

    def print_int(v):
        print(int(v))

    COMMANDS["print:str"] = print_str
    COMMANDS["print:int"] = print_int


def resolve_github(path):
    path = path.replace("github:", "")
    user, repo, file = path.split("/")

    version = "main"
    if "@" in file:
        file, version = file.split("@")

    return f"https://raw.githubusercontent.com/{user}/{repo}/{version}/{file}"


def import_module(target):
    if target == "extra":
        load_extra()
        return

    if target.startswith("github:"):
        url = resolve_github(target)

        os.makedirs(CACHE_DIR, exist_ok=True)
        cache_file = os.path.join(CACHE_DIR, target.replace("/", "_"))

        if os.path.exists(cache_file):
            source = open(cache_file).read()
        else:
            r = requests.get(url)
            if r.status_code != 200:
                raise Exception("Failed to fetch module")

            source = r.text
            open(cache_file, "w").write(source)

        parse_module(source)


def parse_module(source):
    for line in source.splitlines():
        if not line or line.startswith("command") or line.startswith("module"):
            continue

        if line.startswith("command"):
            parts = line.split(",")
            _, name, typ, handler = parts
            COMMANDS[f"{name}:{typ}"] = lambda v: print(v)
