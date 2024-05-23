import chess
import chess.pgn
import chess.variant
import chess.musketeer as Musketeer

board = Musketeer.MusketeerBoard("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")

class Parent():
    def language(self):
        return "Parent"
    def speak(self):
        print(self.language())

class Child(Parent):
    def language(self):
        return "Child"
    
if __name__ == "__main__":
    # child = Child()
    # child.speak()
    # Parent().speak()
    # print (board)
    # print("\n")
    # board.push(chess.Move.from_uci(board, "g7g6"))
    # board.push(chess.Move.from_uci(board, "g2g3"))
    # print(board)
    # print (board.fen())
    # print (Musketeer.MusketeerBoard("rnbqkbkr/pppppppp/8/8/8/8/PPKKPPPP/RNBQKBNR w KQkq - 0 1"))
    # print (Musketeer.MusketeerBoard(board.fen()) == board)
    
    

    board = chess.Board("r3k1nr/ppq1pp1p/2p3p1/8/1PPR4/2N5/P3QPPP/5RK1 b kq b3 0 16")
    #print(board)
    print("****************************************************************************")
    print(str(board.legal_moves))
    print("****************************************************************************")
    #move = chess.Move.from_uci(chess.Board(), "Qxh2+")
    #print(move)
    # print(str(board.legal_moves))
    # moves = str(board.legal_moves)
    # for one in moves:
    #     print(one)
        #if (one == move):
            #print("GOOD")
    

    # setup = "3k4/8/4K3/8/8/8/8/2R5 b - - 0 1"
    # board = chess.Board(setup)
    # print(board)
    # print(board.board_fen())
    # board.push_san("Ke8")
    # print(board)
    # print(board.board_fen())
    # board.push_san("Rc8#")
    # print(board)
    # print(board.board_fen())
    # game = chess.pgn.Game.from_board(board)
    # print(game.headers["FEN"])