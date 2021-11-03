from command_process import *

class Command:
    def __init__(self, name, func, usage):
        self.name = name
        self.func = func
        self.usage = usage 


command = [
    Command("step", com_step, "reg - display registers"),
    Command("quit", com_quit, "quit - exit pendvm"),
]


