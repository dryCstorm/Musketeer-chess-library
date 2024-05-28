from __future__ import annotations
from .squares import *
from .attackmodes import *
import math

Bitboard = int
BB_EMPTY: Bitboard = 0
BB_ALL: Bitboard = 0xffff_ffff_ffff_ffff

BB_A1: Bitboard = 1 << A1
BB_B1: Bitboard = 1 << B1
BB_C1: Bitboard = 1 << C1
BB_D1: Bitboard = 1 << D1
BB_E1: Bitboard = 1 << E1
BB_F1: Bitboard = 1 << F1
BB_G1: Bitboard = 1 << G1
BB_H1: Bitboard = 1 << H1
BB_A2: Bitboard = 1 << A2
BB_B2: Bitboard = 1 << B2
BB_C2: Bitboard = 1 << C2
BB_D2: Bitboard = 1 << D2
BB_E2: Bitboard = 1 << E2
BB_F2: Bitboard = 1 << F2
BB_G2: Bitboard = 1 << G2
BB_H2: Bitboard = 1 << H2
BB_A3: Bitboard = 1 << A3
BB_B3: Bitboard = 1 << B3
BB_C3: Bitboard = 1 << C3
BB_D3: Bitboard = 1 << D3
BB_E3: Bitboard = 1 << E3
BB_F3: Bitboard = 1 << F3
BB_G3: Bitboard = 1 << G3
BB_H3: Bitboard = 1 << H3
BB_A4: Bitboard = 1 << A4
BB_B4: Bitboard = 1 << B4
BB_C4: Bitboard = 1 << C4
BB_D4: Bitboard = 1 << D4
BB_E4: Bitboard = 1 << E4
BB_F4: Bitboard = 1 << F4
BB_G4: Bitboard = 1 << G4
BB_H4: Bitboard = 1 << H4
BB_A5: Bitboard = 1 << A5
BB_B5: Bitboard = 1 << B5
BB_C5: Bitboard = 1 << C5
BB_D5: Bitboard = 1 << D5
BB_E5: Bitboard = 1 << E5
BB_F5: Bitboard = 1 << F5
BB_G5: Bitboard = 1 << G5
BB_H5: Bitboard = 1 << H5
BB_A6: Bitboard = 1 << A6
BB_B6: Bitboard = 1 << B6
BB_C6: Bitboard = 1 << C6
BB_D6: Bitboard = 1 << D6
BB_E6: Bitboard = 1 << E6
BB_F6: Bitboard = 1 << F6
BB_G6: Bitboard = 1 << G6
BB_H6: Bitboard = 1 << H6
BB_A7: Bitboard = 1 << A7
BB_B7: Bitboard = 1 << B7
BB_C7: Bitboard = 1 << C7
BB_D7: Bitboard = 1 << D7
BB_E7: Bitboard = 1 << E7
BB_F7: Bitboard = 1 << F7
BB_G7: Bitboard = 1 << G7
BB_H7: Bitboard = 1 << H7
BB_A8: Bitboard = 1 << A8
BB_B8: Bitboard = 1 << B8
BB_C8: Bitboard = 1 << C8
BB_D8: Bitboard = 1 << D8
BB_E8: Bitboard = 1 << E8
BB_F8: Bitboard = 1 << F8
BB_G8: Bitboard = 1 << G8
BB_H8: Bitboard = 1 << H8
BB_SQUARES: List[Bitboard] = [1 << sq for sq in SQUARES]

BB_CORNERS: Bitboard = BB_A1 | BB_H1 | BB_A8 | BB_H8
BB_CENTER: Bitboard = BB_D4 | BB_E4 | BB_D5 | BB_E5

BB_LIGHT_SQUARES: Bitboard = 0x55aa_55aa_55aa_55aa
BB_DARK_SQUARES: Bitboard = 0xaa55_aa55_aa55_aa55

BB_FILE_A: Bitboard = 0x0101_0101_0101_0101 << 0
BB_FILE_B: Bitboard = 0x0101_0101_0101_0101 << 1
BB_FILE_C: Bitboard = 0x0101_0101_0101_0101 << 2
BB_FILE_D: Bitboard = 0x0101_0101_0101_0101 << 3
BB_FILE_E: Bitboard = 0x0101_0101_0101_0101 << 4
BB_FILE_F: Bitboard = 0x0101_0101_0101_0101 << 5
BB_FILE_G: Bitboard = 0x0101_0101_0101_0101 << 6
BB_FILE_H: Bitboard = 0x0101_0101_0101_0101 << 7
BB_FILES: List[Bitboard] = [BB_FILE_A, BB_FILE_B, BB_FILE_C, BB_FILE_D, BB_FILE_E, BB_FILE_F, BB_FILE_G, BB_FILE_H]

BB_RANK_1: Bitboard = 0xff << (8 * 0)
BB_RANK_2: Bitboard = 0xff << (8 * 1)
BB_RANK_3: Bitboard = 0xff << (8 * 2)
BB_RANK_4: Bitboard = 0xff << (8 * 3)
BB_RANK_5: Bitboard = 0xff << (8 * 4)
BB_RANK_6: Bitboard = 0xff << (8 * 5)
BB_RANK_7: Bitboard = 0xff << (8 * 6)
BB_RANK_8: Bitboard = 0xff << (8 * 7)
BB_RANKS: List[Bitboard] = [BB_RANK_1, BB_RANK_2, BB_RANK_3, BB_RANK_4, BB_RANK_5, BB_RANK_6, BB_RANK_7, BB_RANK_8]

BB_BACKRANKS: Bitboard = BB_RANK_1 | BB_RANK_8


def _sliding_attacks(square: Square, occupied: Bitboard, deltas: Iterable[int], max_step) -> Bitboard:
    attacks = BB_EMPTY

    for delta in deltas:
        sq = square

        for i in range(0, max_step):
            sq += delta
            if not (0 <= sq < 64) or square_distance(sq, sq - delta) > 3:
                break

            attacks |= BB_SQUARES[sq]

            if occupied & BB_SQUARES[sq]:
                break

    return attacks

def _step_attacks(square: Square, deltas: Iterable[int], max_step) -> Bitboard:
    return _sliding_attacks(square, BB_ALL, deltas, max_step)

def _edges(square: Square) -> Bitboard:
    return (((BB_RANK_1 | BB_RANK_8) & ~BB_RANKS[square_rank(square)]) |
            ((BB_FILE_A | BB_FILE_H) & ~BB_FILES[square_file(square)]))

def _carry_rippler(mask: Bitboard) -> Iterator[Bitboard]:
    # Carry-Rippler trick to iterate subsets of mask.
    subset = BB_EMPTY
    while True:
        yield subset
        subset = (subset - mask) & mask
        if not subset:
            break

def _attack_table(deltas: List[int], max_step) -> Tuple[List[Bitboard], List[Dict[Bitboard, Bitboard]]]:
    mask_table: List[Bitboard] = []
    attack_table: List[Dict[Bitboard, Bitboard]] = []

    for square in SQUARES:
        attacks = {}

        mask = _sliding_attacks(square, 0, deltas, max_step) & ~_edges(square)
        for subset in _carry_rippler(mask):
            attacks[subset] = _sliding_attacks(square, subset, deltas, max_step)

        attack_table.append(attacks)
        mask_table.append(mask)

    return (mask_table, attack_table)


BB_KNIGHT_ATTACKS: List[List[List[Bitboard]]] = [[[_step_attacks(sq, [mv], 1) for sq in SQUARES] 
                                                for mv in deltas] 
                                                for deltas in [[17, 10, 15, 6, -17, -10, -15, -6], [-15, -6, -17, -10, 15, 6, 17, 10]]]

BB_LONG_KNIGHT_ATTACKS: List[List[List[Bitboard]]] = [[[_step_attacks(sq, [mv], 1) for sq in SQUARES] 
                                                for mv in deltas] 
                                                for deltas in [[25, 11, 23, 5, -25, -11, -23, -5], [-23, -5, -25, -11, 23, 5, 25, 11]]]

BB_JOKER_ATTACKS: List[List[List[Bitboard]]] = [[[_step_attacks(sq, [mv], 1) for sq in SQUARES] 
                                                for mv in deltas] 
                                                for deltas in [[26, 19, 22, 13, -26, -19, -22, -13], [-22, -13, -26, -19, 22, 13, 26, 19]]]

BB_KING_ATTACKS: List[Bitboard] = [_step_attacks(sq, [9, 8, 7, 1, -9, -8, -7, -1], 1) for sq in SQUARES]

BB_PAWN_ATTACKS: List[List[Bitboard]] = [[_step_attacks(sq, deltas, 1) for sq in SQUARES] for deltas in [[-7, -9], [7, 9]]]

BB_DIAG_MASKS_ATTACKS = [[[_attack_table([mv], len) for len in range(1, MAX_LEN + 1)] 
                                  for mv in deltas] 
                                  for deltas in [[9, 7, -7, -9], [-9, -7, 7, 9]]]

BB_ALFIL_MASKS_ATTACKS = [[[_attack_table([mv], len) for len in range(1, MAX_LEN + 1)] 
                                  for mv in deltas] 
                                  for deltas in [[18, 14, -14, -18], [-18, -14, 14, 18]]]

BB_DIAG3_MASKS_ATTACKS = [[[_attack_table([mv], len) for len in range(1, MAX_LEN + 1)] 
                                  for mv in deltas] 
                                  for deltas in [[27, 21, -21, -27], [-27, -21, 21, 27]]]

BB_ROOK_MASKS_ATTACKS = [[[_attack_table([mv], len) for len in range(1, MAX_LEN + 1)] 
                                  for mv in deltas] 
                                  for deltas in [[-8, 8, -1, 1], [8, -8, 1, -1]]]

BB_DABBABA_MASKS_ATTACKS = [[[_attack_table([mv], len) for len in range(1, MAX_LEN + 1)] 
                                  for mv in deltas] 
                                  for deltas in [[-16, 16, -2, 2], [16, -16, 2, -2]]]

BB_JUMP_MASKS_ATTACKS = [[[_attack_table([mv], len) for len in range(1, MAX_LEN + 1)] 
                                  for mv in deltas] 
                                  for deltas in [[-24, 24, -3, 3], [24, -24, 3, -3]]]


def get_bb_pawn_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    if attackmode & ATTACK_MODE_PAWN:
        attacks |= BB_PAWN_ATTACKS[color][square]
    return attacks

def get_bb_king_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    if attackmode & ATTACK_MODE_KING:
        attacks |= BB_KING_ATTACKS[square]
    return attacks

def get_bb_king_attachs(attackmode, color, square, occupied = 0):
    attacks = 0
    if attackmode & ATTACK_MODE_KING:
        attacks |= BB_KING_ATTACKS[square]
    return attacks

def get_bb_knight_attachs(attackmode, color, square, occupied = 0):
    attacks = 0
    for (mode_id, mode) in enumerate (ATTACK_MODE_KNIGHT):
        if attackmode & mode:
            attacks |= BB_KNIGHT_ATTACKS[color][mode_id][square]
    return attacks

def get_bb_long_knight_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    for (mode_id, mode) in enumerate (ATTACK_MODE_LONG_KNIGHT):
        if attackmode & mode:
            attacks |= BB_LONG_KNIGHT_ATTACKS[color][mode_id][square]
    return attacks

def get_bb_joker_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    for (mode_id, mode) in enumerate (ATTACK_MODE_JOKER):
        if attackmode & mode:
            attacks |= BB_JOKER_ATTACKS[color][mode_id][square]
    return attacks

def get_bb_rook_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    for (mode_id, mode) in enumerate (ATTACK_MODE_ROOK):
        if attackmode & mode:
            type = math.floor (mode_id / MAX_LEN)
            len = mode_id % MAX_LEN
            attacks |= BB_ROOK_MASKS_ATTACKS[color][type][len][1][square][BB_ROOK_MASKS_ATTACKS[color][type][len][0][square] & occupied]
    return attacks

def get_bb_dabbaba_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    for (mode_id, mode) in enumerate (ATTACK_MODE_DABBABA):
        if attackmode & mode:
            type = math.floor (mode_id / MAX_LEN)
            len = mode_id % MAX_LEN
            attacks |= BB_DABBABA_MASKS_ATTACKS[color][type][len][1][square][BB_DABBABA_MASKS_ATTACKS[color][type][len][0][square] & occupied]
    return attacks

def get_bb_jump_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    for (mode_id, mode) in enumerate (ATTACK_MODE_JUMP):
        if attackmode & mode:
            type = math.floor (mode_id / MAX_LEN)
            len = mode_id % MAX_LEN
            attacks |= BB_JUMP_MASKS_ATTACKS[color][type][len][1][square][BB_JUMP_MASKS_ATTACKS[color][type][len][0][square] & occupied]
    return attacks

def get_bb_diag_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    for (mode_id, mode) in enumerate (ATTACK_MODE_DIAG):
        if attackmode & mode:
            type = math.floor (mode_id / MAX_LEN)
            len = mode_id % MAX_LEN
            attacks |= BB_DIAG_MASKS_ATTACKS[color][type][len][1][square][BB_DIAG_MASKS_ATTACKS[color][type][len][0][square] & occupied]
    return attacks

def get_bb_alfil_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    for (mode_id, mode) in enumerate (ATTACK_MODE_ALFIL):
        if attackmode & mode:
            type = math.floor (mode_id / MAX_LEN)
            len = mode_id % MAX_LEN
            attacks |= BB_ALFIL_MASKS_ATTACKS[color][type][len][1][square][BB_ALFIL_MASKS_ATTACKS[color][type][len][0][square] & occupied]
    return attacks

def get_bb_diag3_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    for (mode_id, mode) in enumerate (ATTACK_MODE_DIAG3):
        if attackmode & mode:
            type = math.floor (mode_id / MAX_LEN)
            len = mode_id % MAX_LEN
            attacks |= BB_DIAG3_MASKS_ATTACKS[color][type][len][1][square][BB_DIAG3_MASKS_ATTACKS[color][type][len][0][square] & occupied]
    return attacks

def get_bb_attacks(attackmode, color, square, occupied = 0):
    attacks = 0
    attacks |= get_bb_pawn_attacks(attackmode, color, square, occupied)
    attacks |= get_bb_king_attacks(attackmode, color, square, occupied)
    attacks |= get_bb_knight_attachs(attackmode, color, square, occupied)
    attacks |= get_bb_long_knight_attacks(attackmode, color, square, occupied)
    attacks |= get_bb_joker_attacks(attackmode, color, square, occupied)
    attacks |= get_bb_rook_attacks(attackmode, color, square, occupied)
    attacks |= get_bb_dabbaba_attacks(attackmode, color, square, occupied)
    attacks |= get_bb_jump_attacks(attackmode, color, square, occupied)
    attacks |= get_bb_diag_attacks(attackmode, color, square, occupied)
    attacks |= get_bb_alfil_attacks(attackmode, color, square, occupied)
    attacks |= get_bb_diag3_attacks(attackmode, color, square, occupied)
    return attacks