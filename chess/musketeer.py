from . import *

class MusketeerBoard(Board):
    def __init__(self: BoardT, fen: Optional[str] = STARTING_FEN, *, chess960: bool = False):
        super().__init__(fen)
        