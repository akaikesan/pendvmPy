from pendvm import m, Instruction,FORWARD



def i_add(rsd, rt, u1):
    m.reg[rsd] += m.dir * m.reg[rt]
    return 0

def i_addi(rsd, imm, u1):
    m.reg[rsd] += m.dir * int(imm)
    return 0

def i_andx(rd, rs, rt):
    m.reg[rd] ^= (m.reg[rs] & m.reg[rt])
    return 0

def i_andix(rd, rs, imm):
    m.reg[rd] ^= (m.reg[rs] & int(imm))
    return 0

def i_beq( ra, rb ,off):
    if m.reg[ra] == m.reg[rb] :
        m.BR += off
    return 0

def i_swapbr(r, u1, u2) :
    dirsign = 1 if m.dir == FORWARD else -1 
    tmp = m.BR * dirsign
    m.BR = m.reg[r]
    m.reg[r] = tmp
    return 0

def i_finish(u1, u2, u3):
    if m.dir == -1:
        return 0
    else:
        return -3
