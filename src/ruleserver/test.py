import unittest
import json
import numpy as np

# test imports
from bitboard import Board
from valid_move_check import ValidCheck

global test_data

class FenParserTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def testValidStrings(self):
        for t in test_data["fen"]["validPositions"]:
            exp = {k:np.uint64(int(eval(v),2)) for k,v in t[1].items()}
            b = Board(t[0])
            expBoard = Board()
            expBoard.board.update(exp)
            
            for k,v in exp.items():
                self.assertEqual(b.board[k], v, "\nexpected Board:\n" + str(expBoard) + ", but was actual:\n" + str(b))
    
    def testRepresentation(self):
        for t in test_data["fen"]["validPositions"]:
            exp = {k:np.uint64(int(eval(v),2)) for k,v in t[1].items()}
            expBoard = Board()
            expBoard.board.update(exp)
            
            self.assertEqual(repr(expBoard), t[0])

class MoveCheckTest(unittest.TestCase):
    
    def testMoveCheck(self):
        v = ValidCheck()
        for t in test_data["moveCheck"]:
            board = Board(t[0])
            moves = t[1].split()
            exp = eval(t[2])
            character = board.getField(moves[0])
            
            x_before = 7-int(ord(moves[0][0])-ord("a"))
            y_before = int(moves[0][1])-1
            x_after = 7-int(ord(moves[1][0])-ord("a"))
            y_after = int(moves[1][1])-1
            
            self.assertEqual(v.check_valid_move(character, x_before, y_before, x_after, y_after), exp, "\nBoard representation:\n" + str(board) + "\nmove:"+t[1]+"\ncharacter:"+character+"\nvalid:"+t[2])
    
if __name__ == '__main__':
    with open('test_data.json') as f:
        test_data = json.load(f)
        
    unittest.main()