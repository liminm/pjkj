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
from bitboard import Board

def reihencheckjs(board,player)
    b1='{0:b}'.format((board.board["wh"])).zfill(64)
    b2='{0:b}'.format((board.board["bl"])).zfill(64)
     if  player == "wh":
        for i in range (56, 62):
           if b1(i) != 0:
                return True
        else
          for i=1 to 6:
              if b2(i) !=0:
                 return True
    return False
        
def reihencheckrk(board):
    b = '{0:b}'.format((board.board["k"] & board.board["wh"]) | (board.board["k"] & board.board["bl"])).zfill(64)
    for i in range(55, 63):
        if b[i] != 0:
            return True
    return False

#to do Abklären wie ich an Daten komme vielleicht eigene klasse erstellen
#to do abklären wo mein Code eingebaut wird
#to do FEN Parser verstehen