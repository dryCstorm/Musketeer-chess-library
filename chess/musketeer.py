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
        
        super().__init__(fen)
        
        for custom_param in self.custom_params:
            self.PIECE_TYPES.append(custom_param["piece_id"])
            self.PIECE_SYMBOLS.append(custom_param["letter"].lower())
            self.PIECE_NAMES.append(custom_param["name"])
            self.pieces.append(0)
            print (split_string(custom_param["betza"]))
            
            attack_mode = 0
            for sub in split_string(custom_param["betza"]):
                attack_mode |= self.build_am(sub)
            self.ATTACK_MODES.append(attack_mode)
        #self.ATTACK_MODES.append(ATTACK_MODE_KNIGHT_FH | ATTACK_MODE_ROOK | ATTACK_MODE_KING)
        #self.ATTACK_MODES.append(ATTACK_MODE_KNIGHT_A | ATTACK_MODE_KING)
    
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