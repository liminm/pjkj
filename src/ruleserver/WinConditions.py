#Input:Position bestehend aus: Bitboard der neuen Position      position.position
#                               Spieler der drann ist           position.spieler
#Spieler
#1 = Weiß, Spieler
#0 = Schwarz

# Output: nichts, Weißgewinnt, Schwarzgewinnt

from bitboard import Board

def checkwinJS(self,before,after):              #fen string davor und nach dem zug
    boardafter = getposition(get_figure(before, after))
    playerafter=Board("dein FEN-String-Danach").player
    reihencheck=reihencheckjs(boardafter,playerafter)
    If reihencheckjs:
          if player == w:
            return weißgewinnt
          else schwarzgewinnt
    else return nichts

def reihencheckjs(board,player):
    if  player == w:
        for i=56 to 62:
           if board(i) == 1:
                return true
    else:
        for i=1 to 6:
             if board(i) ==1:
                 return True
    return False

#Racing Kings

#Input:Position bestehend aus: Bitboard der neuen Position
#                               Spieler der drann ist
#Variable Z um Draws zu erkennen
#Output nichts, weißgewinnt,schwarzgewinnt,draw

Z = true
def checkwinRK(self,before, after)
    boardafter=getposition(get_figure(before, after))
    playerafter=Board("dein FEN-String-Danach").player
    reihencheck=reihencheckrk(boardafter,playerafter)
        if Z
            If reihencheck:
                if player== w:
                    Z = false #Variable da weiß gewinnen könnte oder draw
                else:
                    return SchwarzGewinnt
            else:
                   return nichts
        else:
            if reihencheck:
                return draw
            else
                return WeißGewinnt

def reihencheckrk(board):
    b = '{0:b}'.format((board.board["k"] & board.board["wh"]) | (board.board["k"] & board.board["bl"])).zfill(64)
    for i in range(55, 64):
        if b[i] == 1:
            return True
    return False

#to do Abklären wie ich an Daten komme vielleicht eigene klasse erstellen
#to do abklären wo mein Code eingebaut wird
#to do FEN Parser verstehen