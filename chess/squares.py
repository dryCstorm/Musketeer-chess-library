from typing import ClassVar, Callable, Counter, Dict, Generic, Hashable, Iterable, Iterator, List, Literal, Mapping, Optional, SupportsInt, Tuple, Type, TypeVar, Union

MAX_LEN:int = 7
FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANK_NAMES = ["1", "2", "3", "4", "5", "6", "7", "8"]

Square = int
A1: Square = 0
B1: Square = 1
C1: Square = 2
D1: Square = 3
E1: Square = 4
F1: Square = 5
G1: Square = 6
H1: Square = 7
A2: Square = 8
B2: Square = 9
C2: Square = 10
D2: Square = 11
E2: Square = 12
F2: Square = 13
G2: Square = 14
H2: Square = 15
A3: Square = 16
B3: Square = 17
C3: Square = 18
D3: Square = 19
E3: Square = 20
F3: Square = 21
G3: Square = 22
H3: Square = 23
A4: Square = 24
B4: Square = 25
C4: Square = 26
D4: Square = 27
E4: Square = 28
F4: Square = 29
G4: Square = 30
H4: Square = 31
A5: Square = 32
B5: Square = 33
C5: Square = 34
D5: Square = 35
E5: Square = 36
F5: Square = 37
G5: Square = 38
H5: Square = 39
A6: Square = 40
B6: Square = 41
C6: Square = 42
D6: Square = 43
E6: Square = 44
F6: Square = 45
G6: Square = 46
H6: Square = 47
A7: Square = 48
B7: Square = 49
C7: Square = 50
D7: Square = 51
E7: Square = 52
F7: Square = 53
G7: Square = 54
H7: Square = 55
A8: Square = 56
B8: Square = 57
C8: Square = 58
D8: Square = 59
E8: Square = 60
F8: Square = 61
G8: Square = 62
H8: Square = 63
SQUARES: List[Square] = list(range(64))


SQUARE_NAMES = [f + r for r in RANK_NAMES for f in FILE_NAMES]

def parse_square(name: str) -> Square:
    """
    Gets the square index for the given square *name*
    (e.g., ``a1`` returns ``0``).

    :raises: :exc:`ValueError` if the square name is invalid.
    """
    return SQUARE_NAMES.index(name)

def square_name(square: Square) -> str:
    """Gets the name of the square, like ``a3``."""
    return SQUARE_NAMES[square]

def square(file_index: int, rank_index: int) -> Square:
    """Gets a square number by file and rank index."""
    return rank_index * 8 + file_index

def square_file(square: Square) -> int:
    """Gets the file index of the square where ``0`` is the a-file."""
    return square & 7

def square_rank(square: Square) -> int:
    """Gets the rank index of the square where ``0`` is the first rank."""
    return square >> 3

def square_distance(a: Square, b: Square) -> int:
    """
    Gets the Chebyshev distance (i.e., the number of king steps) from square *a* to *b*.
    """
    return max(abs(square_file(a) - square_file(b)), abs(square_rank(a) - square_rank(b)))

def square_manhattan_distance(a: Square, b: Square) -> int:
    """
    Gets the Manhattan/Taxicab distance (i.e., the number of orthogonal king steps) from square *a* to *b*.
    """
    return abs(square_file(a) - square_file(b)) + abs(square_rank(a) - square_rank(b))

def square_knight_distance(a: Square, b: Square) -> int:
    """
    Gets the Knight distance (i.e., the number of knight moves) from square *a* to *b*.
    """
    dx = abs(square_file(a) - square_file(b))
    dy = abs(square_rank(a) - square_rank(b))

    if dx + dy == 1:
        return 3
    elif dx == dy == 2:
        return 4
    elif dx == dy == 1:
        if BB_SQUARES[a] & BB_CORNERS or BB_SQUARES[b] & BB_CORNERS:  # Special case only for corner squares
            return 4

    m = math.ceil(max(dx / 2, dy / 2, (dx + dy) / 3))
    return m + ((m + dx + dy) % 2)

def square_mirror(square: Square) -> Square:
    """Mirrors the square vertically."""
    return square ^ 0x38

SQUARES_180: List[Square] = [square_mirror(sq) for sq in SQUARES]
