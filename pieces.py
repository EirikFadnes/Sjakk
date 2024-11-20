class Piece:
    def __init__(self, team, type, symbol, killable = False):
        self.team = team
        self.type = type
        self.killable = killable
        self.symbol = symbol

    def is_valid_move(self, origin, destination, board):
        raise NotImplementedError("Subclasses must implement this method")
    
    def can_capture(self, origin, destination, board):
        if board.is_enemy(destination, self.team):
            return self.is_valid_move(origin, destination, board)
        return False
        
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
            if board.get_piece((intermediate_x, intermediate_y)) is not None:
                return False  # Path is blocked by another piece

        return True  # Path is clear

class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team, "p", "p")
        self.direction = -1 if team == "White" else 1
    
    def is_valid_move(self, origin, destination, board):
        moving_piece = board.get_piece(origin)
        target_piece = board.get_piece(destination)
        
        # Forward move
        if destination[0] == origin[0]:
            # Move forward by 1 (or by 2 if the pawn is in the starting position)
            if (destination[1] == origin[1] + self.direction) and target_piece is None:
                return True
            if (origin[1] == 1 and moving_piece.team == "Black" or origin[1] == 6 and moving_piece.team == "White") and \
                    destination[1] == origin[1] + (2 * self.direction) and target_piece is None:
                return True     
            else:
                return False
        
        if board.is_enemy(destination, self.team):
            # Capture diagonally
            if abs(destination[0] - origin[0]) == 1 and destination[1] == origin[1] + self.direction:
                if target_piece and target_piece.team != moving_piece.team:
                    return True
            return False
        
        return False


class Rook(Piece):
    def __init__(self, team):
        super().__init__(team, "r", "R")
    
    def is_valid_move(self, origin, destination, board):
        # Ensure movement is either vertical or horizontal
        if origin[0] == destination[0] or origin[1] == destination[1]:
            return self.is_path_clear(origin, destination, board)
        return False


class Knight(Piece):
    def __init__(self, team):
        super().__init__(team, "kn", "H")  # Knights are often represented by 'N' or 'H'
    
    def is_valid_move(self, origin, destination, board):
        moving_piece = board.get_piece(origin)
        target_piece = board.get_piece(destination)
        
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
        moving_piece = board.get_piece(origin)
        target_piece = board.get_piece(destination)
        
        # King can move one square in any direction
        if abs(destination[0] - origin[0]) <= 1 and abs(destination[1] - origin[1]) <= 1:
            if target_piece is None or target_piece.team != moving_piece.team:
                return True
        
        return False