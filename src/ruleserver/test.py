import unittest
import json
import numpy as np

# test imports
from bitboard import Board

global test_data

class FenParserTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def testValidStrings(self):
        for t in test_data["fen"]["validMoves"]:
            exp = {k:np.uint64(int(eval(v),2)) for k,v in t[1].items()}
            b = Board(t[0])
            expBoard = Board()
            expBoard.board.update(exp)
            
            for k,v in exp.items():
                self.assertEqual(b.board[k], v, "\nexpected Board:\n" + str(expBoard) + ", but was actual:\n" + str(b))


if __name__ == '__main__':
    with open('test_data.json') as f:
        test_data = json.load(f)
        
    unittest.main()