import numpy as np
from aes_helper import *

def cipher_glitched(pt, k, g_bit = None):
    """
    Encrypt the plaintext pt using the key k with AES-128 encryption
    Also, force the single bit g_bit to 1 after the first key addition

    See aes.py for sample usage
    """
    Nr = 10
    ks = [keyScheduleRounds(k, 0, r) for r in range(Nr+1)]
    state = pt
    state = [state[i] ^ ks[0][i] for i in range(16)]
    if g_bit is not None and g_bit >= 0 and g_bit < 128:
        byte = g_bit / 8
        bit  = g_bit % 8
        state[byte] |= (1 << bit)
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
    ct = cipher_glitched(pt, k)

    print "Plaintext:"
    printhex(pt)
    print "Key:"
    printhex(k)
    print "Ciphertext:"
    printhex(ct)

    k_attacked = [0x00] * 16
    for byte in range(16):
        for bit in range(8):
            g = byte*8 + bit
            ct_glitched = cipher_glitched(pt, k, g)
            if ct_glitched == ct:
                k_bit = 1
            else:
                k_bit = 0
            k_attacked[byte] |= (k_bit << bit)

            print "Attacking bit %d:" % g
            print "Glitched ciphertext:"
            printhex(ct_glitched)
            print "Recovered bit: %d" % k_bit
            print ""

    print "Original key:"
    printhex(k)
    print "Reconstructed key:"
    printhex(k_attacked)


