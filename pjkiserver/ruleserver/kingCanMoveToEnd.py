from .bitboard import Board
from .racing_kings_check_check import checkmate
from .valid_move_check import ValidCheck

def indexToUci(index):
    return chr(7-(index%8)+97) +  chr(1+(int(index/8))+48)

def kingCanMoveToEnd(board):
    vm = ValidCheck()
    character = "k"
    if (board.player == "w"):
        character = "K"

    pos = board.findCharacter(character)[0]
    x = int(pos%8)
    y = int(pos/8)

    offsets = [[-1, 1], [0,1], [1,1]]
    for o in offsets:
        b_copy = Board(repr(board))
        xNew = x+o[0]
        yNew = y+o[1]

        if x in range(8) and y in range(8):
            index = yNew*8+xNew
            posNew = indexToUci(index)

            b_copy.movePlayer(indexToUci(pos), posNew)
            if vm.check(repr(board), repr(b_copy)) and not checkmate(b_copy) and posNew[1] == '8':
                return True

    return False


