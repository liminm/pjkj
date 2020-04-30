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
    
    def scan(self, string):
        m = self.pattern.match(string)
        
        if m is None:
            raise SyntaxError("The FEN string is not valid!")
        
        
        
        return 
        
    def parse(self, string): # TODO: use the scanner to map string input to bitfields
        pass
        
    def printBitboard(bitboard):
        return '{:064b}'.format(bitboard)