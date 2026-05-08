class Program:
    def __init__(self):
        self.schedule = []
        self.sections = {}

def parse(source: str):
    program = Program()

    lines = source.strip().splitlines()
    program.schedule = lines[0].split("'")

    for line in lines[1:]:
        line = line.strip()
        if line == "!;":
            break

        left, right = line.split(":", 1)
        section, _ = left.split(",")

        program.sections.setdefault(section, []).append(
            right.split(",")
        )

    return program
