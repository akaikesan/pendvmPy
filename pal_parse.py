import sys
from instruction_process import * 


NIL  = 0  # 
REG  = 1  # register
IMM  = 2  # immediate
AMT  = 4  # Expression for the amount to shift by.
OFF  = 8  # 16 bit signed offset 
LOFF = 16 # 26 bit signed offset 

LT = []

class lt:
    def __init__(self, label, address):
        self.label   = label
        self.address = address

instructions = [
    Instruction("ADD",   [REG, REG, NIL], i_add),
    Instruction("ADDI",  [REG, IMM, NIL], i_addi),
    Instruction("ANDX",  [REG, REG, REG], i_andx),
    Instruction("ANDIX",  [REG, REG, IMM], i_andix),
    Instruction("BEQ", [REG, REG, OFF], i_beq),
    Instruction("BGEZ", [REG, OFF, NIL], i_bgez),
    Instruction("BGTZ", [REG, OFF, NIL], i_bgtz),
    Instruction("BLEZ", [REG, OFF, NIL], i_blez),
    Instruction("BLTZ", [REG, OFF, NIL], i_bltz),
    Instruction("BNE", [REG, REG, OFF], i_bne),
    Instruction("BRA", [LOFF, NIL, NIL], i_bra),
    Instruction("EXCH", [REG, REG, NIL], i_exch),
    Instruction("NORX", [REG, REG, REG], i_norx),
    Instruction("NEG", [REG, NIL, NIL], i_neg),
    Instruction("ORX", [REG, REG, REG], i_orx),
    Instruction("ORIX", [REG, REG, IMM], i_orix),
    Instruction("RL", [REG, AMT, NIL], i_rl),
    Instruction("RLV", [REG, REG, NIL], i_rlv),
    Instruction("RR", [REG, AMT, NIL], i_rr),
    Instruction("RRV", [REG, REG, NIL], i_rrv),
    Instruction("SLLX", [REG, REG, AMT], i_sllx),
    Instruction("SLLVX", [REG, REG, REG], i_sllvx),
    Instruction("SLTX", [REG, REG, REG], i_sltx),
    Instruction("SLTIX", [REG, REG, IMM], i_sltix),
    Instruction("SRAX", [REG, REG, AMT], i_srax),
    Instruction("SRAVX", [REG, REG, REG], i_sravx),
    Instruction("SRLX", [REG, REG, AMT], i_srlx),
    Instruction("SRLVX", [REG, REG, REG], i_srlvx),
    Instruction("SUB", [REG, REG, NIL], i_sub),
    Instruction("XOR", [REG, REG, NIL], i_xorx),
    Instruction("XORI", [REG, IMM, NIL], i_xorix),
    Instruction("SWAPBR", [REG, NIL, NIL], i_swapbr),
    Instruction("RBRA", [LOFF, NIL, NIL], i_rbra),
    Instruction("OUTPUT", [REG, NIL, NIL], i_show),
    Instruction("SHOW", [REG, NIL, NIL], i_show),
    Instruction("START",  [NIL,NIL,NIL], i_start),
    Instruction("FINISH",  [NIL,NIL,NIL], i_finish),
    Instruction( None,   [REG, IMM, NIL], None),
]



def parse_inst(label, inst, args):

    i = 0
    while (i < len(instructions)):
        if instructions[i].inst.lower() == inst.lower():
            break
        i += 1
    if instructions[i].inst == None:
        print("undefined instruction")
        sys.exit()
    
    j = 0
    a = []
    while (j < 3):
        if instructions[i].args[j] == NIL:
            a.append(0)
        elif instructions[i].args[j] == REG:
            reg = parse_reg(args[j])
            if reg == -1 :
                print("unexpected register")
                return -1
            elif reg == -2:
                print("register out of range")
                return -1
            else:
                a.append(reg)
        elif instructions[i].args[j] == IMM or instructions[i].args[j] == AMT:
            a.append(parse_immed(args[j]))

        elif instructions[i].args[j] == OFF or instructions[i].args[j] == LOFF:
            absolute = parse_immed(args[j])
            if absolute == None:
                print("bad offset")
                return -1
            else:
                a.append(absolute - m.PC)

        j += 1
    
    return instructions[i].func(a[0], a[1], a[2])


def parse_reg(reg):
    if(reg[0] != '$'):
        return -1
    
    r = int(reg[1:len(reg)])

    if r >= 0 and r <= 31:
        return r
    else:
        return -2

def parse_immed(immed):

    if(immed == None):
        return None
    elif (immed == ""):
        return None

    temp = parse_label(immed)
    if(temp == None):
        try:
            return int(immed)
        except:
            return None
    else : 
        return temp

def parse_label(label):
    
    for l in LT:
        if (l.label == label):
            return l.address

    return None            

