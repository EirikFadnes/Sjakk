from pieces import Rook, Bishop, Queen, Knight, Pawn, King
import string

class Board:
    def __init__(self):
        self.turn = 0  
        self.team_to_move = "White"   
        self.next_team_to_move = "Black"
        self.team_in_check = None   
        self.board_state = {
            (0, 0): Rook("Black"), (1, 0): Knight("Black"),
            (2, 0): Bishop("Black"), (3, 0): King("Black"),
            (4, 0): Queen("Black"), (5, 0): Bishop("Black"),
            (6, 0): Knight("Black"), (7, 0): Rook("Black"),
            (0, 1): Pawn("Black"), (1, 1): Pawn("Black"),
            (2, 1): Pawn("Black"), (3, 1): Pawn("Black"),
            (4, 1): Pawn("Black"), (5, 1): Pawn("Black"),
            (6, 1): Pawn("Black"), (7, 1): Pawn("Black"),

            (0, 6): Pawn("White"), (1, 6): Pawn("White"),
            (2, 6): Pawn("White"), (3, 6): Pawn("White"),
            (4, 6): Pawn("White"), (5, 6): Pawn("White"),
            (6, 6): Pawn("White"), (7, 6): Pawn("White"),
            (0, 7): Rook("White"), (1, 7): Knight("White"),
            (2, 7): Bishop("White"), (3, 7): King("White"),
            (4, 7): Queen("White"), (5, 7): Bishop("White"),
            (6, 7): Knight("White"), (7, 7): Rook("White")
        }

    
    def get_piece(self, position):
        return self.board_state.get(position, None)
    

    def is_empty(self, position):
        return self.get_piece(position) is not None
    
    
    def is_enemy(self, position, team):
        piece = self.get_piece(position)
        return piece is not None and piece.team != team


    def display(self):
        
        def print_red(skk): print("\033[91m {}\033[00m" .format(skk), end = " ")
        def print_green(skk): print("\033[92m {}\033[00m" .format(skk), end = " ")
        def print_square(color):
            if color == "Black":
                print("\u2591"*2, end = " ")
            if color == "White":
                print("\u2588"*2, end = " ")

        print()
        print(f"Turn {self.turn}: {self.team_to_move}'s turn to move.")
        letters = list(string.ascii_uppercase[:8]) # Coordinate letters
        print(" ", " ".join(f"{letter} " for letter in letters)) # Print letters above board
        for row in range(8):
            print(8-row, end = " ") # Print coordinates on left side of board
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
            print(8-row, end = "") # Print coordinates on right side of board
            print()  # New line after each row
        print(" ", " ".join(f"{letter} " for letter in letters)) # Print letters below board
        print() # New line after each board


    def check_valid_move(self, origin, destination):
        moving_piece = self.get_piece(origin)

        if not moving_piece:
            print("No piece at origin.")
            return False
        
        if moving_piece.team != self.team_to_move:
            print("It's not your turn!")
            return False
        
        if not self.is_on_board(destination):
            print("Destination is off the board.")
            return False
        
        if not moving_piece.is_valid_move(origin, destination, self):
            print("Invalid move for the piece.")
            return False

        if self.team_in_check == self.team_to_move and not self.can_move_uncheck(origin, destination):
            return False

        # If all checks pass, the move is valid
        return True
    

    def can_move_uncheck(self, origin, destination):
        moving_piece = self.get_piece(origin)
        target_piece = self.get_piece(destination)
        
        # Simulate the move
        self.board_state[destination] = moving_piece
        self.board_state[origin] = None

        # Check if still ckecked
        king_position = self.find_king(self.team_to_move)
        still_checked = self.check_if_checked(king_position)

        # Undo move
        self.board_state[origin] = moving_piece
        self.board_state[destination] = target_piece

        if still_checked:
            return False
        else: 
            return True


    def increment_turn(self):
        self.turn += 1
        # Swap teams
        self.team_to_move, self.next_team_to_move = self.next_team_to_move, self.team_to_move


    def is_on_board(self, destination):
        if destination[0] < 0 or destination[0] > 8 or destination[1] < 0 or destination[1] > 8:
            return False
        else:
            return True
        

    def other_team(team):
        if team == "Black":
            return "White"
        if team == "White":
            return "Black"
        else: 
            return False
        
    
    def get_all_possible_moves(self, piece, origin):
            possible_moves = []
            for row in range(8):
                for col in range(8):
                    destination = (row, col)
                    if piece.is_valid_move(origin, destination, self.board_state):
                        possible_moves.append(destination)
            return possible_moves
    

    def find_king(self, team):
        for col in range(8):
            for row in range(8):
                piece_to_check = self.get_piece((col, row))
                if piece_to_check.__class__.__name__ == "King" and piece_to_check.team == team:
                    return (col, row)
        return False

        
    def check_if_checked(self, king_position):       
        # Check if any piece of the current team can attack the opponent's king
        for position, piece in self.board_state.items():
            if piece and piece.team == self.next_team_to_move:  # Only check pieces from the current team
                if piece.can_capture(position, king_position, self):
                    print(f"The {self.team_to_move} king is checked!")
                    return True  # The king is threatened (in check)
        return False  # The king is not threatened
    
        
    def update_team_in_check(self):
        king_position = self.find_king(self.team_to_move)
        if self.check_if_checked(king_position):
            self.team_in_check = self.team_to_move
    

    def get_king_moves(self, king_position):
        row, col = king_position
        possible_moves = [
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
            (row, col - 1),                     (row, col + 1),
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
        ]
        moves = []
        for move in possible_moves:
            if self.is_on_board(move):
                if self.board_state.get(move).team != self.team_to_move:
                    if self.check_if_checked(move) == False:
                        moves.append(move)
        return moves


    def check_if_check_mate(self):
        # Check if the current player's king is in check
        if not self.check_if_checked():
            return False  # No check, so not checkmate
        
        # Find the position of the king
        king_position = self.find_king(self.team_to_move)
        
        # Check if the king can move to any adjacent square to escape check
        king_moves = self.get_king_moves(king_position)
        for move in king_moves:
            if self.is_on_board(move) and not self.check_if_checked(move):
                return False  # The king can move to safety, so not checkmate
        
        # If the king can't escape, check if any piece can block or capture the attacking piece
        for origin, piece in self.board_state.items():
            if piece and piece.team == self.team_to_move:
                for move in self.get_all_possible_moves(piece, origin):
                    if self.is_on_board(move):
                        # Simulate the move
                        saved_state = self.board_state[move]
                        self.board_state[move] = piece
                        self.board_state[origin] = None
                        
                        # Check if this move stops the check
                        if not self.check_if_checked():
                            # Undo the move
                            self.board_state[origin] = piece
                            self.board_state[move] = saved_state
                            return False  # A move can block or capture the threat, so not checkmate
                        
                        # Undo the move
                        self.board_state[origin] = piece
                        self.board_state[move] = saved_state
        
        # If no valid move can block or escape the check, it's checkmate
        return True

            
    def move_piece(self, origin, destination):
        print(f"Orgin: {origin}")
        print(f"Destination: {destination}")
        self.update_team_in_check()
        moving_piece = self.get_piece(origin)
        if not moving_piece:
            print("No piece to move at the origin.")
            return False

        if self.check_valid_move(origin, destination):
            target_piece = self.get_piece(destination)
            if target_piece:
                if moving_piece.can_capture(origin, destination, self):
                    print(f"Captured {target_piece.__class__.__name__}!")
                else:
                    print("Invalid capture attempt.")
                    return False
            # Perform the move
            self.board_state[destination] = moving_piece
            del self.board_state[origin]
            self.increment_turn()
            self.display()
            return True
        return False
   
