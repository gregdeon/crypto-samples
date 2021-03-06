import numpy as np
from aes_helper import *

def cipher(pt, k):
    """
    Encrypt the plaintext pt using the key k with AES-128 encryption
    Both inputs must be length-16 lists with one byte in each element

    Example:
        pt = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        k = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 
             0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
        ct = cipher(pt, k)
    """
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

def printhex(x):
    """
    Print the list x as a single hex string

    Example: 
        Input: printhex([0x01, 0x02, 0xab, 0xff])
        Output: "0x0102abff"
    """
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
