import numpy as np
from aes_helper import *

def cipher(pt, k):
    Nr = 10
    ks = [keyScheduleRounds(k, 0, r) for r in range(Nr+1)]
    state = pt
    state = [state[i] ^ ks[0][i] for i in range(16)]
    for r in range(1, Nr):
        state = subbytes(state)
        state = shiftrows(state)
        state = mixcolumns(state)
        state = [state[i] ^ ks[r][i] for i in range(16)]
    state = subbytes(state)
    state = shiftrows(state)
    state = [state[i] ^ ks[Nr][i] for i in range(16)]
    return state

def process(fname, b, m, max_threads):
    # Note: we assume fixed key here for huge speedup
    ks = [keyScheduleRounds(key[0], 0, r) for r in range(11)]
    c = [AL.cipher(pt[i], ks) for i in range(numtraces)]
    
def printhex(x):
    print "0x" + "".join(["%02x"%b for b in x])

if __name__ == "__main__":
    pt = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    k = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 
         0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
    ct = cipher(pt, k)

    printhex(pt)
    printhex(k)
    printhex(ct)
