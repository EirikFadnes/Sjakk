
class Piece:
    def __init__(self, team, type, symbol, killable = False):
        self.team = team
        self.type = type
        self.killable = killable
        self.symbol = symbol
    
bp = Piece('b', 'p', 'p')
wp = Piece('w', 'p', 'p')
bk = Piece('b', 'k', 'K')
wk = Piece('w', 'k', 'K')
br = Piece('b', 'r', 'R')
wr = Piece('w', 'r', 'R')
bb = Piece('b', 'b', 'B')
wb = Piece('w', 'b', 'B')
bq = Piece('b', 'q', 'Q')
wq = Piece('w', 'q', 'Q')
bkn = Piece('b', 'kn', 'H')
wkn = Piece('w', 'kn', 'H')




class Board:
    def __init__(self):
        self.board_state = {
            (0, 0): br, (1, 0): bkn,
            (2, 0): bb, (3, 0): bk,
            (4, 0): bq, (5, 0): bb,
            (6, 0): bkn, (7, 0): br,
            (0, 1): bp, (1, 1): bp,
            (2, 1): bp, (3, 1): bp,
            (4, 1): bp, (5, 1): bp,
            (6, 1): bp, (7, 1): bp,

            (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
            (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
            (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
            (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
            (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
            (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
            (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
            (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

            (0, 6): wp, (1, 6): wp,
            (2, 6): wp, (3, 6): wp,
            (4, 6): wp, (5, 6): wp,
            (6, 6): wp, (7, 6): wp,
            (0, 7): wr, (1, 7): wkn,
            (2, 7): wb, (3, 7): wk,
            (4, 7): wq, (5, 7): wb,
            (6, 7): wkn, (7, 7): wr
        }

    def display(self):
        
        def print_red(skk): print("\033[91m {}\033[00m" .format(skk), end = " ")
        def print_green(skk): print("\033[92m {}\033[00m" .format(skk), end = " ")
        def print_square(color):
            if color == "b":
                print("\u2591"*2, end = " ")
            if color == "w":
                print("\u2588"*2, end = " ")

        print() # turn info
        for row in range(8):
            for col in range(8):
                piece = self.board_state.get((col, row), None)
                if piece:
                    if piece.team == "b":
                        print_red(piece.symbol)
                    elif piece.team == "w":
                        print_green(piece.symbol)
                    else:
                        raise ValueError(f"Invalid team of piece. Expected 'b' or 'w', got '{piece.team}'")
                else:
                    if (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0):
                        print_square("b")
                    else:
                        print_square("w")
            print()  # New line after each row
    
    def move_piece(self, origin, destination):
        piece = self.board_state.get(origin)
        if piece:
            if destination[0] < 0 or destination[0] > 8 or destination[1] < 0 or destination[1] > 8:
                raise ValueError("Destination out of bounds")
            self.board_state[destination] = piece
            self.board_state[origin] = None
        else:
            print("No piece at the origin.")

    
        
board = Board()
#board.display()
board.move_piece((0, 1), (0, 3))  # Move a pawn
board.display()



