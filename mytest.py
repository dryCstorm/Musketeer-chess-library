import chess

board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")

class Parent():
    def language(self):
        return "Parent"
    def speak(self):
        print(self.language())

class Child(Parent):
    def language(self):
        return "Child"
    
if __name__ == "__main__":
    child = Child()
    child.speak()
    Parent().speak()
    print (board)
    print("\n")
    board.push(chess.Move.from_uci("g1f3"))
    print (board)