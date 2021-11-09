import sys
from memory import mem_get, memory, MEM_DATA, MEM_INST
from pal_parse import lt, LT, parse_inst
from pendvm import m, FORWARD, REVERSE, EXEC_FINISH, EXEC_INVALID_INST,EXEC_ERROR,EXEC_NORMAL





def load_imem(input):

    address = -1
    inst_offset = -1
    error_flag = 0

    with open(input) as f:
        if ";; pendulum pal file\n" != str(f.readline()):
            print("Input file is not in Pendulum pal format.\n");
            sys.exit()
        line = 0
        for l in f:
            line += 1
            l = strip_comments(l)
            fields = l.strip().split()
            if len(fields) == 0 :
                continue

            if fields[0] == ".start":
                global start_point
                start_point = fields[1]
                continue

            #something is on this line 
            address += 1

            if fields[0][len(fields[0])-1] == ':':
                mem = mem_get(address)
                mem.label = fields[0][0:len(fields[0])-1]
                # stuff the label table 
                LT.append(lt(mem.label, address))
                inst_offset = 1 # if label is not null, fields has instruction from index 1 not 0.
                if len(fields) == 1:
                    address -= 1 # get next line 
                    continue     # the memory has label and a instruction on next line 
            else:
                inst_offset = 0
        
            mem = mem_get(address)

            if fields[inst_offset].lower() == "data":
                mem.type = MEM_DATA
            
                if len(fields) - inst_offset != 2 :
                    print("poorly formatted dw declaration")
                    error_flag += 1
                    continue
                mem.value = fields[inst_offset + 1]
                continue
            else:
                # regular instruction
                mem.type = MEM_INST
                mem.inst = fields[inst_offset]
                i = 1 + inst_offset
                while (i < len(fields)):
                    mem.args[i-1-inst_offset] = fields[i]
                    i += 1
            continue

def step_processor(iterations):
    loop = True
    if iterations < 0:
        loop = False
        iterations = 1

    m.reset = False
    while (iterations > 0):
        result = execute_instruction()
        mem = mem_get(m.PC)
        if loop:
            iterations -= 1
        if(result == EXEC_FINISH):
            return EXEC_FINISH
        elif result == EXEC_ERROR:
            return EXEC_ERROR
    return EXEC_NORMAL



def strip_comments(line):
    i = 0
    for l in line:
        if(l == ";"):
            line = line[0:i]
            break
        i += 1   
    return line

def execute_instruction():
    mem = mem_get(m.PC)
    if mem.type != MEM_INST:
        print("no instruction")
        sys.exit()
    
    status = parse_inst(mem.label, mem.inst, mem.args)
    
    if status == 0:
        adjust_pc()
    if status == -1:
        return EXEC_INVALID_INST
    elif status == -3:
        return EXEC_FINISH
    elif status == -4:
        return EXEC_ERROR



def adjust_pc():
    if  m.BR == 0:
        if m.dir == FORWARD:
            m.PC += 1
        else:
            m.PC -= 1
    else:
        m.PC += m.BR
    
    if m.externaldir == FORWARD:
        m.time += 1
    else:
        m.time -= 1
