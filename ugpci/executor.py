from ugpip import import_module, COMMANDS

class Executor:
    def __init__(self, program):
        self.program = program
        self.state = {}

    def run_instruction(self, instr):
        cmd = instr[0]

        if cmd == "set":
            _, key, value = instr
            self.state[key] = value

        elif cmd == "import":
            _, target = instr
            import_module(target)

        elif cmd == "print":
            _, typ, value = instr
            key = f"print:{typ}"

            if key in COMMANDS:
                COMMANDS[key](value)
            else:
                raise Exception(f"Unknown command {key}")

    def run(self):
        # run config (section 1)
        for instr in self.program.sections.get("1", []):
            self.run_instruction(instr)

        # run execution sections
        for sec in self.program.schedule[1:]:
            for instr in self.program.sections.get(sec, []):
                self.run_instruction(instr)
