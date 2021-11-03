from machine import step_processor
from memory import mem_get, MEM_INST
from pendvm import m, MAX_REG

import sys

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
            step = int(args[1])
        except:
            print("1st argument is not int.")
            return 0
         
        display_state()
        step_processor(step)
        com_reg([])

    return 0


def com_reg(args):
    i=0
    j=0

    while i < MAX_REG:
        print("${:02d}".format(i)+ "={:08X}".format(int(m.reg[i])),"\t", end = ' ')
        i += 1
        j += 1
        if j==4 :
            j = 0
            print("")
    print("")
    print("STEP#: "+str(m.time),"\t","PC: {:08X}".format(int(m.PC)),"\t","BR: {:08X}".format(int(m.BR)),"\t",end = '')
    if m.dir == 1:
        print(" DIR : FORWARD")
    else:
        print(" DIR : REVERSE")
    
    return 0
    
def com_quit(args):
    print("Exit Pendulum VM? (y/n) ", end='')
    buffer = input()
    if buffer == 'y':
        sys.exit()
    return 0
