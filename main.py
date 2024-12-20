
from board import Board
import string


def translate_coordinate(coordinate):
    letters = list(string.ascii_uppercase[:8])
    nums_8_1 = list(reversed(range(1, 9)))
    nums_0_7 = list(range(0, 7))

    lookup_letter = dict(zip(letters, nums_0_7))
    lookup_number = dict(zip(nums_8_1, nums_0_7))

    coordinate = coordinate.upper()
    letter = coordinate[0]
    number = int(coordinate[1])

    x = lookup_letter.get(letter)
    y = lookup_number.get(number)
    res = (x, y)
    
    return res
    


 
        
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
    [(3, 0), (2, 0)],
    [(1, 3), (1, 2)],
    [(7, 1), (7, 3)],
    [(1, 2), (1, 1)],
    [(3, 0), (4, 0)]
]


mode = input("Mode:")
if mode == "test":
    for move in moves:
        origin, destination = move
        board.move_piece(origin, destination)

if mode == "game":
    while 1 == 1:
        origin = input("Input origin:")
        destination = input("Input destination:")
        origin = translate_coordinate(origin)
        destination = translate_coordinate(destination)
        board.move_piece(origin, destination)