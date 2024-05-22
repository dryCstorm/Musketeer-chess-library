import chess.musketeer as Musketeer

board = Musketeer.MusketeerBoard()

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