'''
Jumpsturdy
input:board ,player
player "wh" oder "bl"
output true => Gewinnzustand
        false => kein Gewinnzustand spiel geht weiter
Racing Kings
input board 
output true false
'''
import numpy as np
from bitboard import Board



def reihencheckjs(board , player=None):
    mask1 = np.uint64(9079256848778919936)
    mask2 = np.uint64(126)
    if player==None:
        player = board.player
    if player == 'w':
        if (board.board["wh"] & mask1) > 0:
            return True
    else:
        if (board.board["bl"] & mask2) > 0:
            return True

    return False


def reihencheckrk(board):
    mask=1111111100000000000000000000000000000000000000000000000000000000
    if (board.board["k"] & mask) > 0:
            return True
    return False


#to do Abklären wie ich an Daten komme vielleicht eigene klasse erstellen
#to do abklären wo mein Code eingebaut wird
#to do FEN Parser verstehen