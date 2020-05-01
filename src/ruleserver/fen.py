import numpy as np
import re

"""
Notation:
a trun will alway be FEN i.e: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1    
we start at the top row number 8
small letters for the black figuees and capital letters for white 
r - rook (Turm), n - knight(Springer), b - bishop(laeufer), q - queen (Koenigin), k - king (koenig)
--> racing king is not played with pawns
an 8 is tells us the amount of empty fields, if we have a king on the third tile from the left : 2k5
the first letter after the board description is the current player
the KQkq we can ignore and will be replaced with - (chess only rules)
the - wont be changed (again chess rules that do not apply to racing kings)
the 0 is the amount of halfturns since the last figure was killed TODO languge 
1 the round number that is currently played
"""
class Board:
    
    def __init__(self, string=None):
        self.start = "8/8/8/8/8/8/krbnKRBN/qrbnQRBN w - - 0 1"
        self.string = string
        self.board = {
            "q": np.int64(0),
            "k": np.int64(0),
            "p": np.int64(0),
            "b": np.int64(0),
            "k": np.int64(0),
            "r": np.int64(0),
            "w": np.int64(0),
            "b": np.int64(0)
        }
        
        self.pattern = re.compile("([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8}) ([wb]) (\-|KQ?k?q?|K?Qk?q?|K?Q?kq?|K?Q?k?q) (\-|[a-f][1-8]) (\d+) (\d+)")
        
        if not string is None:
            self.parse(string)
            
    def resetBoard(self):
        self.string = self.start
        self.parse(self.string)
        
    """
    return [0-7:    Figurenstellung aus der FEN Notation,
            8:      Spieler am Zug,
            9:      Rochade,
            10:     En passant,
            11:     Halbzüge
            12:     Zugnummer]
    """
    def scan(self, string):
        m = self.pattern.match(string)
        
        if m is None:
            raise SyntaxError("The FEN string is not valid!")
            
        return [m.group(i) for i in range(1, int(self.pattern.groups+1) )]
        
    def checkFigures(self, lines):
        if len(lines) != 8:
            return False
        
        for l in lines:
            figures = 0
            for c in l:
                if c.isdigit():
                    figures+= int(c)
                else:
                    figures+=1
                
            if figures != 8:
                return False
        return True
        
    def parse(self, string): # TODO: use the scanner to map string input to bitfields
        
        fen = string
        if not isinstance(string, list):
            self.string = string
            fen = self.scan(string)
        
        if not checkFigures(fen[:8]):
            raise ValueError("ParseError: Each line on the board has to contain exactly 8 fields.")
        
        # fen ist ab hier eine liste, im im kommentar über der scan funktion beschriebenend format
        # du kannst auch python fen.py ausführen, dann siehst du einen beispielaufruf von fen
           
    def to_matrix(self, board_str):
        self.vector = []
        self.matrix = []
        for char in board_str:
            if char.isdigit():
                for i in range(int(char)):
                    self.vector.append(" ")
            elif char == "/":
                self.matrix.append(self.vector)
                self.vector = []
            else:
                self.vector.append(char)
        self.matrix.append(self.vector)
        return self.matrix
           
    def printBoard(self, bitboard):
        board = '{0:b}'.format(bitboard).zfill(64)
        board = board[::-1]
        indices = [0,8,16,24,32,40,48,56,]
        parts = [board[i:j] for i,j in zip(indices, indices[1:]+[None])]
        rows = [8,7,6,5,4,3,2,1]
        for i in range(1,9):
            parts[i-1] = str(rows[i-1])+'|'+ parts[i-1]
        parts.insert(0,"  abcdefgh")
        print('\n'.join(parts))
    
    # TODO: not working with this implementation yet. Has to rely on bitboards
    def to_matrix(self, board_str):
        self.vector = []
        self.matrix = []
        for char in board_str:
            if char.isdigit():
                for i in range(int(char)):
                    self.vector.append(" ")
            elif char == "/":
                self.matrix.append(self.vector)
                self.vector = []
            else:
                self.vector.append(char)
        self.matrix.append(self.vector)
        return self.matrix
"""
main function
is only called if you directly execute this code, not just if you import it
"""
if __name__ == "__main__": 
    b = Board()
    sample = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    s = b.scan(sample)
    print(s)
    print(b.checkFigures(s[:8]))