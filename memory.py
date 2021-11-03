
MEM_EMPTY = 0
MEM_DATA = 1
MEM_INST = 2


memory = []


class Memory:
    def __init__(self, address):
        self.address    = address
        self.label      = ""
        self.type       = MEM_EMPTY
        self.breakpoint = 0
        self.value      = 0
        self.inst       = ""
        self.args       = ["", "", ""]



def mem_get(address):
    for mem in memory:
        if mem.address == address:
            return mem
    
    memory.append(Memory(address))
    return memory[-1]