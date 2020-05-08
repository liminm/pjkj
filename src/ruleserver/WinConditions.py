#Input:Position bestehend aus: Bitboard der neuen Position      position.position
#                               Spieler der drann ist           position.spieler
#Spieler
#1 = Weiß, Spieler
#0 = Schwarz

# Output: nichts, Weißgewinnt, Schwarzgewinnt

def checkwinJS(self,before,after):              #fen string davor und nach dem zug
    boardafter = getposition(get_figure(before, after))
    playerafter=Board("dein FEN-String-Danach").player
    reihencheck=reihencheckjs(boardafter,playerafter)
    If reihencheck:
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
                 returrn true
    return false

#Racing Kings

#Input:Position bestehend aus: Bitboard der neuen Position
#                               Spieler der drann ist
#Variable Z um Draws zu erkennen
#Output nichts, weißgewinnt,schwarzgewinnt,draw

Z = true
def checkwinRK(self,position, Z)
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

def reihencheckrk(board,player):
    for i= 55 to 63:
        if board(i) == 1:
            return true
    return false

#to do Abklären wie ich an Daten komme vielleicht eigene klasse erstellen
#to do abklären wo mein Code eingebaut wird
#to do FEN Parser verstehen