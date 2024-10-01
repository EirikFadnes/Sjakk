
class Piece:
    def __init__(self, team, type, symbol, killable = False):
        self.team = team
        self.type = type
        self.killable = killable
        self.symbol = symbol
        
    def is_path_clear(self, origin, destination, board):
        # Check if the path from origin to destination is clear (i.e., no pieces in the way).
        x1, y1 = origin
        x2, y2 = destination

        dx = x2 - x1
        dy = y2 - y1

        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

        # Calculate the number of steps to reach the destination
        steps = max(abs(dx), abs(dy))

        # Traverse each square along the path to check for blocking pieces
        for step in range(1, steps):
            intermediate_x = x1 + step * step_x
            intermediate_y = y1 + step * step_y
            if board.get((intermediate_x, intermediate_y)) is not None:
                return False  # Path is blocked by another piece

        return True  # Path is clear

class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team, "p", "p")
    
    def is_valid_move(self, origin, destination, board):
        moving_piece = board.get(origin)
        target_piece = board.get(destination)
        direction = -1 if moving_piece.team == "White" else 1

        # Forward move
        if destination[0] == origin[0]:
            # Move forward by 1 (or by 2 if the pawn is in the starting position)
            if (destination[1] == origin[1] + direction) and target_piece is None:
                return True
            if (origin[1] == 1 and moving_piece.team == "Black" or origin[1] == 6 and moving_piece.team == "White") and \
                    destination[1] == origin[1] + (2 * direction) and target_piece is None:
                return True     
            else:
                return False
        
        # Capture diagonally
        if abs(destination[0] - origin[0]) == 1 and destination[1] == origin[1] + direction:
            if target_piece and target_piece.team != moving_piece.team:
                return True
        
        return False

class Rook(Piece):
    def __init__(self, team):
        super().__init__(team, "r", "R")
    
    def is_valid_move(self, origin, destination, board):
        # Ensure movement is either vertical or horizontal
        if origin[0] == destination[0] or origin[1] == destination[1]:
            if self.is_path_clear(origin, destination, board):
                return True
        return False

class Knight(Piece):
    def __init__(self, team):
        super().__init__(team, "kn", "H")  # Knights are often represented by 'N' or 'H'
    
    def is_valid_move(self, origin, destination, board):
        moving_piece = board.get(origin)
        target_piece = board.get(destination)
        
        # Knight moves in an "L" shape (2 squares in one direction and 1 in the other)
        if (abs(destination[0] - origin[0]) == 2 and abs(destination[1] - origin[1]) == 1) or \
           (abs(destination[0] - origin[0]) == 1 and abs(destination[1] - origin[1]) == 2):
            # Empty square or capture an enemy piece
            if target_piece is None or target_piece.team != moving_piece.team:
                return True
        
        return False


class Bishop(Piece):
    def __init__(self, team):
        super().__init__(team, "b", "B")
    
    def is_valid_move(self, origin, destination, board):
        # Ensure movement is diagonal
        if abs(destination[0] - origin[0]) == abs(destination[1] - origin[1]):
            if self.is_path_clear(origin, destination, board):
                return True
        return False


class Queen(Piece):
    def __init__(self, team):
        super().__init__(team, "q", "Q")
    
    def is_valid_move(self, origin, destination, board):
        # Queen can move like both a rook (vertical/horizontal) and a bishop (diagonal)
        if (origin[0] == destination[0] or origin[1] == destination[1]) or \
           (abs(destination[0] - origin[0]) == abs(destination[1] - origin[1])):
            if self.is_path_clear(origin, destination, board):
                return True
        return False


class King(Piece):
    def __init__(self, team):
        super().__init__(team, "k", "K")
    
    def is_valid_move(self, origin, destination, board):
        moving_piece = board.get(origin)
        target_piece = board.get(destination)
        
        # King can move one square in any direction
        if abs(destination[0] - origin[0]) <= 1 and abs(destination[1] - origin[1]) <= 1:
            if target_piece is None or target_piece.team != moving_piece.team:
                return True
        
        return False


class Board:
    def __init__(self):
        self.turn = 0  
        self.team_to_move = "White"      
        self.board_state = {
            (0, 0): Rook("Black"), (1, 0): Knight("Black"),
            (2, 0): Bishop("Black"), (3, 0): King("Black"),
            (4, 0): Queen("Black"), (5, 0): Bishop("Black"),
            (6, 0): Knight("Black"), (7, 0): Rook("Black"),
            (0, 1): Pawn("Black"), (1, 1): Pawn("Black"),
            (2, 1): Pawn("Black"), (3, 1): Pawn("Black"),
            (4, 1): Pawn("Black"), (5, 1): Pawn("Black"),
            (6, 1): Pawn("Black"), (7, 1): Pawn("Black"),

            (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
            (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
            (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
            (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
            (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
            (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
            (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
            (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

            (0, 6): Pawn("White"), (1, 6): Pawn("White"),
            (2, 6): Pawn("White"), (3, 6): Pawn("White"),
            (4, 6): Pawn("White"), (5, 6): Pawn("White"),
            (6, 6): Pawn("White"), (7, 6): Pawn("White"),
            (0, 7): Rook("White"), (1, 7): Knight("White"),
            (2, 7): Bishop("White"), (3, 7): King("White"),
            (4, 7): Queen("White"), (5, 7): Bishop("White"),
            (6, 7): Knight("White"), (7, 7): Rook("White")
        }


    def display(self):
        
        def print_red(skk): print("\033[91m {}\033[00m" .format(skk), end = " ")
        def print_green(skk): print("\033[92m {}\033[00m" .format(skk), end = " ")
        def print_square(color):
            if color == "Black":
                print("\u2591"*2, end = " ")
            if color == "White":
                print("\u2588"*2, end = " ")

        print()
        print(f"Turn {self.turn}: {self.team_to_move} to move.")

        for row in range(8):
            for col in range(8):
                piece = self.board_state.get((col, row), None)
                if piece:
                    if piece.team == "Black":
                        print_red(piece.symbol)
                    elif piece.team == "White":
                        print_green(piece.symbol)
                    else:
                        raise ValueError(f"Invalid team of piece. Expected 'Black' or 'White', got '{piece.team}'")
                else:
                    if (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0):
                        print_square("Black")
                    else:
                        print_square("White") 
            print()  # New line after each row
        print() # New line after each board

    def check_valid_move(self, origin, destination):
        moving_piece = self.board_state.get(origin)
        target_piece = self.board_state.get(destination)
        if moving_piece.is_valid_move(origin, destination, self.board_state): 
            return True 
        else: 
            return False

        

    def increment_turn(self):
        self.turn += 1
        if self.turn % 2 == 0:
            self.team_to_move = "White"
        else:
            self.team_to_move = "Black"

    def is_on_board(self, destination):
        if destination[0] < 0 or destination[0] > 8 or destination[1] < 0 or destination[1] > 8:
            return False
        else:
            return True

    
    def move_piece(self, origin, destination):
        print(f"Orgin: {origin}")
        print(f"Destination: {destination}")
        moving_piece = self.board_state.get(origin)
        target_piece = self.board_state.get(destination)
        if moving_piece and self.check_valid_move(origin, destination):
            if self.team_to_move == moving_piece.team:
                if self.is_on_board(destination):
                    if target_piece is None or target_piece.team != moving_piece.team:  # Valid move or capture
                        self.board_state[destination] = moving_piece
                        self.board_state[origin] = None
                        if target_piece:
                            print(f"Captured {target_piece.__class__.__name__}!")
                        self.increment_turn()
                        self.display()
                        return True
                    else:
                        print("You cannot move to a square occupied by your own piece.")
                        return False
                else:
                    print("Destination out of bounds")
                    return False
            else:
                print("Wrong color to move")
                return False
        else:
            print("No valid move or no piece at the origin.")
            return False


    
        
board = Board()
moves = [
    [(0, 6), (0, 4)],
    [(1, 1), (1, 3)],
    [(0, 4), (1, 3)],
    [(1, 0), (2, 2)],
    [(0, 7), (0, 1)],
    [(0, 0), (0, 1)],
    [(1, 6), (1, 5)],
    [(2, 0), (0, 2)],
    [(4, 6), (4, 4)],
    [(3, 0), (2, 0)]
]
for move in moves:
    origin, destination = move
    board.move_piece(origin, destination)

