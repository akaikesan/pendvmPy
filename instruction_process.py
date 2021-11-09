from pendvm import m, Instruction,FORWARD
from memory import MEM_INST, mem_get
import numpy as np

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

def i_bgez(rb, off, u1):
    if m.reg[rb] >= 0 :
        m.BR += off
    return 0    
    
def i_bgtz( rb,  off,  u1):
    if m.reg[rb] > 0 :
        m.BR += off
    return 0

def i_blez( rb,  off,  u1):
    if m.reg[rb] <= 0 :
        m.BR += off
    return 0

def i_bltz( rb,  off,  u1):
    if m.reg[rb] < 0 :
        m.BR += off
    return 0

def i_bne( ra,  rb,  off):
    if m.reg[ra] != m.reg[rb] :
        m.BR += off
    return 0

def i_bra( loff,  u1,  u2):
    m.BR += loff
    return 0

def i_exch(rd, ra, u1):
    loc = mem_get(m.reg[ra])
    if loc.type == MEM_INST:
        return -4
    tmp = m.reg[rd]
    m.reg[rd] = loc.value
    loc.value = tmp
    return 0

def i_norx(rd, rs, rt):
    m.reg[rd] ^= ~(m.reg[rs] | m.reg[rt])
    return 0

def i_neg(rsd, u1, u2):
    m.reg[rsd] *= -1
    return 0

def i_orx(rd, rs, rt):
    m.reg[rd] ^= m.reg[rs] | m.reg[rt]
    return 0

def i_orix(rd, rs, imm):
    m.reg[rd] ^= (m.reg[rs] | imm)
    return 0

def i_rl(rsd, amt ,u1):
    a = m.reg[rsd]
    if m.reg[rsd] < 0:
        a *= -1
        a = np.invert(a, dtype = np.uint32) + 1
    if m.dir == FORWARD:
        if amt != 0:
            m.reg[rsd] = np.left_shift(a, amt, dtype = np.uint32) | (EXTRACT(a,32-amt, 31) )
    else:
        if amt != 0:
            m.reg[rsd] = np.right_shift(a, amt, dtype = np.uint32) | (EXTRACT(a,0,amt -1) << (32 - amt))
    # value in reg is int32.
    m.reg[rsd] = np.bitwise_or(m.reg[rsd],0, dtype = np.int32)

    return 0

def i_rlv(rsd, rt ,u1):
    a = m.reg[rsd]
    if m.reg[rsd] < 0:
        a *= -1
        a = np.invert(a, dtype =np.uint32) + 1

    if m.dir == FORWARD:
        if m.reg[rt] != 0:
            m.reg[rsd] = np.left_shift(a, m.reg[rt], dtype = np.uint32) | (EXTRACT(a,32-m.reg[rt], 31) )
    else:
        if m.reg[rt] != 0:
            m.reg[rsd] = np.right_shift(a, m.reg[rt], dtype = np.uint32) | (EXTRACT(a,0,m.reg[rt] -1) << (32 - m.reg[rt]))
    
    # value in reg is int32.
    m.reg[rsd] = np.bitwise_or(m.reg[rsd],0, dtype = np.int32)
    return 0

def i_rr(rsd, amt ,u1):
    a = m.reg[rsd]
    if m.reg[rsd] < 0:
        a *= -1
        a = np.invert(a, dtype =np.uint32) + 1
    if m.dir == FORWARD:
        if amt != 0:
            m.reg[rsd] = np.right_shift(a, amt, dtype = np.uint32) | (EXTRACT(a,0,amt -1) << (32 - amt))
    else:
        if amt != 0:
            m.reg[rsd] = np.left_shift(a, amt, dtype = np.uint32) | (EXTRACT(a,32-amt, 31) )
    
    # value in reg is int32.
    m.reg[rsd] = np.bitwise_or(m.reg[rsd],0, dtype = np.int32)

    return 0



def i_rrv(rsd, rt ,u1):
    a = m.reg[rsd]
    if m.reg[rsd] < 0:
        a *= -1
        a = np.invert(a, dtype =np.uint32) + 1
    print(bin(a))

    if m.dir == FORWARD:
        if m.reg[rt] != 0:
            m.reg[rsd] = np.right_shift(a, m.reg[rt], dtype = np.uint32) | (EXTRACT(a,0,m.reg[rt] -1) << (32 - m.reg[rt]))
    else:
        if m.reg[rt] != 0:
            m.reg[rsd] = np.left_shift(a, m.reg[rt], dtype = np.uint32) | (EXTRACT(a,32-m.reg[rt], 31) )
    
    # value in reg is int32.
    m.reg[rsd] = np.bitwise_or(m.reg[rsd],0, dtype = np.int32)

    return 0


def i_sllx(rd, rs, amt):
    m.reg[rd] ^= (2**31 << amt)
    m.reg[rd] = np.bitwise_or(m.reg[rd],0, dtype = np.int32)
    return 0

def i_sllvx(rd, rs, rt):
    m.reg[rd] ^= m.reg[rs] << m.reg[rt]
    m.reg[rd] = np.bitwise_or(m.reg[rd],0, dtype = np.int32)
    return 0

def i_sltx(rd, rs, rt):
    if (m.reg[rs] < m.reg[rt]):
        m.reg[rd] ^= 1
    return 0

def i_sltix(rd, rs, imm):
    if (m.reg[rs] < imm):
        m.reg[rd] ^= 1
    return 0
# right shift. consider unsigned or signed.
# signed
def i_srax(rd, rs, amt):
    i = 0
    tmp = m.reg[rs] >> amt
    # when left most bit is 1, fill in with 1.
    if EXTRACT(m.reg[rs],31,31) == 1:
        i = (2^amt - 1) << (32 - amt)
    # example) when amt is 2 , i is 11000000000000000000000000000000.
    tmp |= i

    m.reg[rd] ^= tmp
    print(m.reg[rd])
    return 0
# signed 
def i_sravx(rd, rs, rt):
    i = 0
    tmp = m.reg[rs] >> m.reg[rt]
    # when left most bit is 1, fill in with 1.
    if EXTRACT(m.reg[rs],31,31) == 1:
        i = (2^m.reg[rt] - 1) << (32 - m.reg[rt])
    tmp |= i

    m.reg[rd] ^= tmp
    return 0


# unsigned, fill in with 0 
def i_srlx(rd, rs, amt):
    a = m.reg[rs]
    if a < 0:
        a *= -1
        a = np.invert(a, dtype = np.uint32) + 1
    m.reg[rd] ^= np.bitwise_or(a >> amt,0, dtype = np.int32)
    return 0

# unsigned, fill in with 0 
def i_srlvx (rd, rs, rt):
    a = m.reg[rs]
    if a < 0:
        a *= -1
        a = np.invert(a, dtype = np.uint32) + 1
    m.reg[rd] ^= np.bitwise_or(a >> m.reg[rt],0, dtype = np.int32)
    return 0


def i_sub( rsd,  rt,  u1):
    m.reg[rsd] -= (m.dir)*(m.reg[rt])
    return 0

def i_xorx( rsd,  rt,  u1):
    m.reg[rsd] ^= int(m.reg[rt])
    return 0

def i_xorix( rsd,  imm,  u1):
    m.reg[rsd] ^= imm
    return 0

def i_swapbr(r, u1, u2) :
    dirsign = 1 if m.dir == FORWARD else -1 
    tmp = m.BR * dirsign
    m.BR = m.reg[r] * dirsign
    m.reg[r] = tmp
    return 0

def i_show(r, u1, u2):
    print(m.reg[r])
    return 0

def i_rbra(loff, u1, u2):
    m.BR += loff
    m.dir = -(m.dir)
    return 0

def i_start(u1, u2, u3):
    if m.dir == 1:
        return 0
    else:
        return -3

def i_finish(u1, u2, u3):
    if m.dir == -1:
        return 0
    else:
        return -3


def EXTRACT(num, low, high):
    a = num >> low
    b = (2 << (high - low)) - 1
    return a & b