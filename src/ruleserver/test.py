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
        """
        t[0] == fen string für board vor moveCheck
        t[1] == move in uci mit space separated
        t[2] == says if the move should be valid
        """
        v = ValidCheck()
        for t in test_data["moveCheck"]+test_data["sampleGame"]:
            board = Board(t[0])
            board_moved = Board(t[0])
            moves = (t[1], t[2])
            board_moved.moveUCI(moves[0], moves[1])
            exp = eval(t[3])
            character = board.getField(moves[0])
            
            self.assertEqual(v.check(repr(board), repr(board_moved)), exp, "\nBoard representation before move:\n" + str(board) + "\nboard representation after move:\n"+ str(board_moved) + "\nmove:"+t[1]+"\ncharacter:"+character+"\nvalid:"+t[2])
    
if __name__ == '__main__':
    with open('test_data.json') as f:
        test_data = json.load(f)
        
    unittest.main()