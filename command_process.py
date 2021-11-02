from machine import step_processor
from memory import mem_get, MEM_INST
from pendvm import m

def display_state():
    mem = mem_get(m.PC)
    i = 0
    print("MEM(PC):", mem.inst, '', end='')
    while(i < 3):
        print(mem.args[i], '', end='')
        i += 1
    
    if (mem.type != MEM_INST):
        print("--NO INSTRUCTION--")
    if( mem.breakpoint == 1):
        print("\t*BREAK*")
    print("\n")


def com_step(args):
    if(len(args) > 0):
        try:
            step_processor(int(args[1]))
        except:
            print("1st argument is not int.")
            return 0
        display_state()
    return 0