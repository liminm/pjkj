#Input:Position bestehend aus: Bitboard der neuen Position      position.position
#                               Spieler der drann ist           position.spieler
#Spieler
#1 = Weiß, Spieler
#0 = Schwarz

# Output: nichts, Weißgewinnt, Schwarzgewinnt

function checkwinJS(position):
    if allowed(position):                   #ist der Zug erlaubt
       If  reihencheckjs(position):
            if position.spieler == 1:
                return weißgewinnt
        else schwarzgewinnt
    else
        return nichts

funtion reihencheckjs(position):
    if position.spieler == 1:
       for i= 56 to 62:
           if position.position(i) == 1:
                returrn true
    else:
        for i=1 to 6:
             if position.position(i) == 1:
                 returrn true
    return false

#Racing Kings

#Input:Position bestehend aus: Bitboard der neuen Position
#                               Spieler der drann ist
#Variable Z um Draws zu erkennen
#Output nichts, weißgewinnt,schwarzgewinnt,draw

Z = true
function checkwinRK(position, Z)
    if allowed(position) # ist eingegebener Zug valide
        if Z
            If reihencheckrk(position):
                if position.Spieler == 1:
                    Z = false #Variable da weiß gewinnen könnte oder draw
                else:
                    return SchwarzGewinnt
            else:
                   return nichts
        else:
            if reihencheck(position):
                return draw
            else
                return WeißGewinnt

function reihencheckrk(position):
    for i= 55 to 63:
        if position.position(i) == 1:
            return true
        else
            return false