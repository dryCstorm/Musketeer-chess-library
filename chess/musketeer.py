from chess import PieceType, Square
from . import *


class MusketeerBoard(Board):
    # custom_pieces example
    # [{
    #   name:"Elephant",
    #   letter:"E",
    #   betza:"fhHfrlRK",
    #   position:[2, 3] // Black and White
    # },
    # {
    #   name:"Unicorn",
    #   letter:"U",
    #   betza:"NK"
    #   init_position: [6, 4]
    # }
    # ]
    
    def build_am(self, betza):
        return build_am_from_betza(betza)     
        
    def __init__(self: BoardT, custom_pieces, fen: Optional[str] = STARTING_FEN, *, chess960: bool = False):
        self.custom_params = custom_pieces.copy()
        
        for i, custom_param in enumerate(self.custom_params):
            custom_param.setdefault("current_position", custom_param ["position"].copy())
            custom_param.setdefault("piece_id", len(self.PIECE_TYPES) + i + 1)
            custom_param ["current_position"] = custom_param ["position"].copy()
        
        for custom_param in self.custom_params:
            self.PIECE_TYPES.append(custom_param["piece_id"])
            self.PIECE_SYMBOLS.append(custom_param["letter"].lower())
            self.PIECE_NAMES.append(custom_param["name"])
            
            attack_mode = 0
            for sub in split_string(custom_param["betza"]):
                attack_mode |= self.build_am(sub)
            self.ATTACK_MODES.append(attack_mode)
            
        super().__init__(fen)
    
    def set_muskeeter_chess_init_position(self, positions):
        for i, custom_param in enumerate(self.custom_params):
            custom_param["position"] = positions [i].copy()
            custom_param["current_position"] = positions [i].copy()
        
    def inplaced_musketeer_pieces (self):
        res = []
        for custom_param in self.custom_params:
            if custom_param ["current_position"][0] != None:
                res.append((custom_param["letter"].lower(), custom_param["current_position"][0], 9))
            if custom_param ["current_position"][1] != None:
                res.append((custom_param["letter"].upper(), custom_param["current_position"][1], 0))
            
        return res
    
    def reset(self):
        for custom_param in self.custom_params:
            custom_param["current_position"] = custom_param["position"].copy()
        super().reset()
        
    def _remove_piece_at(self, square: int) -> int | None:
        res = super()._remove_piece_at(square)
        if res != None and self.piece_at(square) == None:
            for custom_param in self.custom_params:
                if custom_param ["current_position"][1] != None and square == custom_param ["current_position"][1] - 1:    
                    self._set_piece_at(square, custom_param["piece_id"], True)
                    custom_param ["current_position"][1] = None
                if custom_param ["current_position"][0] != None and square == 56 + custom_param ["current_position"][0] - 1:    
                    self._set_piece_at(square, custom_param["piece_id"], False)
                    custom_param ["current_position"][0] = None
        return res
    
    def _set_board_fen(self, fen: str) -> None:
        print("fen : ", fen)
        # Compatibility with set_fen().
        fen = fen.strip()
        if " " in fen:
            raise ValueError(f"expected position part of fen, got multiple parts: {fen!r}")

        # Ensure the FEN is valid.
        rows = fen.split("/")
        if len(rows) != 10:
            raise ValueError(f"expected 10 rows in position part of fen: {fen!r}")

        # Validate each row.
        for row in rows[1:9]:
            field_sum = 0
            previous_was_digit = False
            previous_was_piece = False

            for c in row:
                if c in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                    if previous_was_digit:
                        raise ValueError(f"two subsequent digits in position part of fen: {fen!r}")
                    field_sum += int(c)
                    previous_was_digit = True
                    previous_was_piece = False
                elif c == "~":
                    if not previous_was_piece:
                        raise ValueError(f"'~' not after piece in position part of fen: {fen!r}")
                    previous_was_digit = False
                    previous_was_piece = False
                elif c.lower() in self.PIECE_SYMBOLS:
                    field_sum += 1
                    previous_was_digit = False
                    previous_was_piece = True
                else:
                    raise ValueError(f"invalid character in position part of fen: {fen!r}")

            if field_sum != 8:
                raise ValueError(f"expected 8 columns per row in position part of fen: {fen!r}")

        # Clear the board.
        self._clear_board()

        # Put pieces on the board.
        square_index = 0
        for c in "/".join(rows[1:9]):
            if c in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                square_index += int(c)
            elif c.lower() in self.PIECE_SYMBOLS:
                piece = Piece.from_symbol(self, c)
                self._set_piece_at(SQUARES_180[square_index], piece.piece_type, piece.color)
                square_index += 1
            elif c == "~":
                self.promoted |= BB_SQUARES[SQUARES_180[square_index - 1]]
        
        square_index = 0
        for c in rows[0]:
            square_index += 1
            if c != "*":
                for custom_param in self.custom_params:
                    if custom_param["letter"].lower() == c:
                        custom_param["current_position"][0] = square_index
                        break
                    
        
        square_index = 0
        for c in rows[9]:
            square_index += 1
            if c != "*":
                for custom_param in self.custom_params:
                    if custom_param["letter"] == c:
                        custom_param["current_position"][1] = square_index
                        break

        
    def board_fen(self, *, promoted: Optional[bool] = False) -> str:
        """
        Gets the board FEN (e.g.,
        ``rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR``).
        """
        builder: List[str] = []
        empty = 0
        
        bfen = "********/"
        for custom_param in self.custom_params:
            if custom_param["current_position"][0] != None:
                index = custom_param["current_position"][0] - 1
                bfen = bfen[:index] + custom_param["letter"].lower() + bfen[index+1:]
        builder.append(bfen)
        
        for square in SQUARES_180:
            piece = self.piece_at(square)

            if not piece:
                empty += 1
            else:
                if empty:
                    builder.append(str(empty))
                    empty = 0
                builder.append(piece.symbol())
                if promoted and BB_SQUARES[square] & self.promoted:
                    builder.append("~")

            if BB_SQUARES[square] & BB_FILE_H:
                if empty:
                    builder.append(str(empty))
                    empty = 0

                if square != H1:
                    builder.append("/")



        wfen = "/********"
        for custom_param in self.custom_params:
            if custom_param["current_position"][1] != None:
                index = custom_param["current_position"][1]
                wfen = wfen[:index] + custom_param["letter"] + wfen[index+1:]
        builder.append(wfen)
        return "".join(builder)