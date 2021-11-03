FORWARD = 1
REVERSE = -1
MAX_REG = 32

EXEC_NORMAL = 1
EXEC_FINISH = 3
EXEC_ERROR = 4
EXEC_INVALID_INST = 5

class Machine:
    def __init__(self, PC, BR, dir,externaldir, reset, time):
        self.PC   = PC
        self.BR   = BR
        self.dir  = dir
        self.externaldir = externaldir
        self.reset  = reset
        self.time = time
        self.reg  = [0] * MAX_REG # 0-31 register

m = Machine(0, 0, FORWARD, FORWARD, True, 0)

class Instruction :
    def __init__(self, inst, args, func):
        self.inst = inst
        self.args  = args
        self.func = func

