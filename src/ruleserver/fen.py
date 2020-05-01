import numpy as np
import re

class Board:
    
    def __init__(self, string=None):
        self.string = string
        self.queen = np.int64(0)
        self.king = np.int64(0)
        self.pawn = np.int64(0)
        self.bishop = np.int64(0)
        self.knight = np.int64(0)
        self.rook = np.int64(0)
        self.color = np.int64(0)
        
        self.pattern = re.compile("([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8}) ([wb]) (\-|KQ?k?q?|K?Qk?q?|K?Q?kq?|K?Q?k?q) (\-|[a-f][1-8]) (\d+) (\d+)")
        
        if not string is None:
            self.parse(string)
    """
    return [0-8:    Figurenstellung aus der FEN Notation,
            9:      Spieler am Zug,
            10:     Rochade,
            11:     En passant,
            12:     Halbzüge
            13:     Zugnummer]
    """
    def scan(self, string):
        m = self.pattern.match(string)
        
        if m is None:
            raise SyntaxError("The FEN string is not valid!")
            
        return [m.group(i) for i in range(1, int(self.pattern.groups+1) )]
        
    def parse(self, string): # TODO: use the scanner to map string input to bitfields
        pass
        
    def printBitboard(bitboard):
        return '{:064b}'.format(bitboard)
        
        
if __name__ == "__main__":
    b = Board()
    print(b.scan("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))