import functools
import re
from .squares import *

def build_am (mask, mask_length, array, reach_length = MAX_LEN):
    res = 0
    step = int(len(array) / mask_length)
    for i in range(0, mask_length):
        for j in range(0, min(step, reach_length)):
            res |= array [i * step + j] if mask & (1 << (mask_length - 1 - i)) else 0
    return res


# For Black
ATTACK_MODE_PAWN = 1 << 0
ATTACK_MODE_BISHOP = 1 << 1
ATTACK_MODE_KING = 1 << 2
ATTACK_MODE_KNIGHT = [1 << i for i in range(100, 108)]
ATTACK_MODE_LONG_KNIGHT = [1 << i for i in range(200, 208)]
ATTACK_MODE_JOKER = [1 << i for i in range(300, 308)]
ATTACK_MODE_ROOK = [1 << i for i in range(400, 400 + 4 * MAX_LEN)]
ATTACK_MODE_DABBABA = [1 << i for i in range(500, 500 + 4 * MAX_LEN)]
ATTACK_MODE_JUMP = [1 << i for i in range(600, 600 + 4 * MAX_LEN)]
ATTACK_MODE_DIAG = [1 << i for i in range(700, 700 + 4 * MAX_LEN)]
ATTACK_MODE_ALFIL = [1 << i for i in range(800, 800 + 4 * MAX_LEN)]
ATTACK_MODE_DIAG3 = [1 << i for i in range(900, 900 + 4 * MAX_LEN)]

#   6 7 | 4 5
#   ---------
#   2 3 | 0 1
#   NS      S

(   KNIGHT_A,   KNIGHT_FF,  KNIGHT_FS,  KNIGHT_FH,  KNIGHT_BB,  KNIGHT_BS,  KNIGHT_BH,  KNIGHT_LS,  KNIGHT_RS,  KNIGHT_LH,  KNIGHT_RH) = [
    0b11111111, 0b00001010, 0b00000101, 0b00001111, 0b10100000, 0b01010000, 0b11110000, 0b00100010, 0b01000100, 0b00110011, 0b11001100
]

#       0    
#   2-------3
#       1    

(   ROOK_A, ROOK_F, ROOK_B, ROOK_L, ROOK_R) = [
    0b1111, 0b1000, 0b0100, 0b0010, 0b0001
]

#   4   |   3
#   ---------
#   2   |   1

(   DIAG_A,  DIAG_FL, DIAG_FR, DIAG_BL, DIAG_BR, DIAG_FH, DIAG_BH, DIAG_LH, DIAG_RH) = [
    0b1111,  0b0001,  0b0010,  0b0100,  0b1000,  0b0011,  0b1100,  0b0101,  0b1010
]


def split_string (str):   
    return functools.reduce(lambda x, y: x + re.findall(r'[a-z]+[A-Z]\d|[a-z]+[A-Z]|[A-Z]\d|[A-Z]', y), re.findall(r'[a-zA-Z]+\d+|[a-zA-Z]+$', str), [])

def build_am_from_betza(betza):
    length = 7
    piece = ""
    params = ""
    if betza [len(betza) - 1].isdigit():
        length = int(betza [len(betza) - 1])
        betza = betza[0:-1]
    piece = betza[len(betza) - 1]
    params = betza [0:-1]
    
    if (piece == "K"):
        return ATTACK_MODE_KING
    if (piece == "W" or piece == "R" or piece == "D" or piece == "H"):
        array = ATTACK_MODE_ROOK
        if piece == "D":
            array = ATTACK_MODE_DABBABA
        if piece == "H":
            array = ATTACK_MODE_JUMP
        res = 0
        res |= build_am(ROOK_F, 4, array, length) if "f" in params else 0
        res |= build_am(ROOK_B, 4, array, length) if "b" in params else 0
        res |= build_am(ROOK_L, 4, array, length) if "l" in params else 0
        res |= build_am(ROOK_R, 4, array, length) if "r" in params else 0
        
        return build_am(ROOK_A, 4, array, length) if res == 0 else res
    if (piece == "F" or piece == "A" or piece == "Q"):
        array = ATTACK_MODE_DIAG
        if piece == "A":
            array = ATTACK_MODE_ALFIL
        if piece == "Q":
            array = ATTACK_MODE_DIAG3
        if "f" in params and "l" in params:
            return build_am(DIAG_FL, 4, array, length)
        if "f" in params and "r" in params:
            return build_am(DIAG_FR, 4, array, length)
        if "b" in params and "l" in params:
            return build_am(DIAG_BL, 4, array, length)
        if "b" in params and "r" in params:
            return build_am(DIAG_BR, 4, array, length)
        if "f" in params:
            return build_am(DIAG_FH, 4, array, length)
        if "b" in params:
            return build_am(DIAG_BH, 4, array, length)
        if "l" in params:
            return build_am(DIAG_LH, 4, array, length)
        if "r" in params:
            return build_am(DIAG_RH, 4, array, length)
        return build_am(DIAG_A, 4, array, length)
    if (piece == "N" or piece == "L" or piece == "J"):
        array = ATTACK_MODE_KNIGHT
        if piece == "L":
            array = ATTACK_MODE_LONG_KNIGHT
        if piece == "J":
            array = ATTACK_MODE_JOKER
        if "s" in params:
            if "f" in params:
                return build_am(KNIGHT_FS, 8, array)
            if "b" in params:
                return build_am(KNIGHT_BS, 8, array)
            if "l" in params:
                return build_am(KNIGHT_LS, 8, array)
            if "r" in params:
                return build_am(KNIGHT_RS, 8, array)
        if "h" in params:
            if "f" in params:
                return build_am(KNIGHT_FH, 8, array)
            if "b" in params:
                return build_am(KNIGHT_BH, 8, array)
            if "l" in params:
                return build_am(KNIGHT_LH, 8, array)
            if "r" in params:
                return build_am(KNIGHT_RH, 8, array)
        res = 0
        res |= build_am(KNIGHT_FF, 8, array) if "f" in params else 0
        res |= build_am(KNIGHT_BB, 8, array) if "b" in params else 0
        res |= build_am(KNIGHT_LS, 8, array) if "l" in params else 0
        res |= build_am(KNIGHT_RS, 8, array) if "r" in params else 0
        
        return build_am(KNIGHT_A, 8, array) if res == 0 else res
    
    return 0