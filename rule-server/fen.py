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
        
        self.pattern = re.compile("([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8})\/([1-8rnbqkpPRNBQK]{1,8}) ([wb]) (\-|K?Q?k?q?) (\-|[a-f][1-8]) (\d+) (\d+)")
        
        if not string is None:
            self.parse(string)
    
    def scan(self, string):
        m = self.pattern.match(string)
        
        if m is None:
            print("String could not be parsed!!!!")
            return None
        
    def parse(self, string): # TODO: use the scanner to map string input to bitfields
        pass