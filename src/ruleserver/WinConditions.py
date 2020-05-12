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

def reihencheckjs(board,player):
    mask1=0111111000000000000000000000000000000000000000000000000000000000
    mask2 = 0000000000000000000000000000000000000000000000000000000001111110
    if  player == "wh":
        if (board.board["wh"] & mask1) > 0:
            return True
        else:
            for i in
                if (board.board["bl"] & mask2) >0:
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