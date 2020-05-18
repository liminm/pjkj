'''
Jumpsturdy
input:board ,player
player "w" oder "b"
output true
        false
Racing Kings
input board
output true false
'''
import numpy as np

from .bitboard import Board


MASKJS1 = np.uint64(9079256848778919936)
MASKJS2 = np.uint64(126)
def reihencheckjs(board , player=None):
    if player==None:
        player = board.player
    if player == 'w':
        if board.board["wh"] & MASKJS1 != 0:
            return True
    else:
        if board.board["bl"] & MASKJS2 != 0:
            return True

    return False

MASKRK = np.uint64(int("1"*8 + "0"*8*7,2))

def reihencheckrk(board):
    if board.board["k"] & MASKRK != 0:
        return True
    return False


#to do Abklären wie ich an Daten komme vielleicht eigene klasse erstellen
#to do abklären wo mein Code eingebaut wird
#to do FEN Parser verstehen
