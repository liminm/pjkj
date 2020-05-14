import unittest
import json
import numpy as np

# test imports
from bitboard import Board
from valid_move_check import ValidCheck
from WinConditions import reihencheckrk
from WinConditions import reihencheckjs
from racing_kings_check_check import KingIsAttackedCheck

global test_data

class FenParserTest(unittest.TestCase):
    
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
    
    def testSetField(self):
        """
        tests if setField sets the correct field
        t[0] = location on the field (f2)
        t[1] = symbol of the figure (q)
        t[2] = string representation of the figures bitboard
        """

        for t in test_data["fen"]["testSetField"]:
            board = Board()
            board.setField(t[0], t[1])
            self.assertEqual(board.board[t[1].lower()], int(t[2], base = 2))
            if t[1].lower() == t[1]:
                self.assertEqual(board.board["bl"], int(t[2], base = 2))
            else:
                self.assertEqual(board.board["wh"], int(t[2], base=2))

    def testGetField(self):
        """
        tests if board.getField returns the correct figure ()
        t[0] = a FEN string to set the field
        t[1] = position
        t[2] = correct figure
        """

        for t in test_data["fen"]["testGetField"]:
            board = Board(t[0])
            self.assertEqual(board.getField(t[1]), t[2])
    
    def testScan(self):
        """
        tests if board.scan split a FEN string correct
        tests if board.scan raises an error when the syntax of a FEN is incorrect
        t[0] = FEN String
        t[1] = expected array
        """
        board = Board()
        pos = 0
        for t in test_data['fen']['testScan']:
            if pos < 2:
                self.assertEqual(board.scan(t[0]), t[1])
            else:
                self.assertRaises(SyntaxError, board.scan, t[0])
            pos += 1
    
    # TODO: the Board.movePlayer function simulates the given UCI move and changes all relevant information in the fen string
    # this function is called in the moveCheck to simulate a move
    def testMovePlayer(self):
        pass

class MoveCheckTest(unittest.TestCase):
    
    def testMoveCheckRacingKings(self):
        """
        t[0] == fen string für board vor moveCheck
        t[1] == move in uci mit space separated
        t[2] == says if the move should be valid
        """
        v = ValidCheck()
        for t in test_data["racingKings"]["moveCheck"]+test_data["racingKings"]["sampleGame"]:
            board = Board(t[0])
            board_moved = Board(t[0])
            moves = (t[1], t[2])
            board_moved.moveUCI(moves[0], moves[1])
            exp = eval(t[3])
            character = board.getField(moves[0])
            
            self.assertEqual(v.check(repr(board), repr(board_moved)), exp, "\nBoard representation before move:\n" + str(board) + "\nboard representation after move:\n"+ str(board_moved) + "\nmove:"+t[1]+"\ncharacter:"+character+"\nvalid:"+t[2])
    
    # TODO: has to be implemented
    def testMoveCheckJumpStirdy(self):
        v = ValidCheck()
        for t in test_data["jumpStirdy"]["moveCheck"] + test_data["jumpStirdy"]["sampleGame"]:
            board = Board(t[0])
            board_moved = Board(t[0])
            uci = t[1] + t[2]
            board_moved.moveUCI(uci)
            exp = eval(t[3])
            character = board.getField(t[1])
            
            self.assertEqual(v.check(repr(board), uci, "JS"), exp, "\nBoard representation before move:\n" + str(board) + "\nboard representation after move:\n"+ str(board_moved) + "\nmove:"+t[1]+"\ncharacter:"+character+"\nvalid:"+t[2])

class WinConditionsTest(unittest.TestCase):
    
    def testRacingKings(self):
        """
        """
        for t in test_data["racingKings"]["winConditions"]:
            board = Board(t[0])
            expected = eval(t[1])
            
            self.assertEqual(reihencheckrk(board), expected, "\nBoard representation:\n" + str(board) + "\nexpected:"+t[1])
    
    def testJumpStirdy(self):
        """
        """
        for t in test_data["jumpStirdy"]["winConditions"]:
            board = Board(t[0])
            player = None # w | b
            expected = eval(t[1])
            
            self.assertEqual(reihencheckjs(board, player), expected, "\nBoard representation:\n" + str(board) + "\nexpected:"+t[1])

class checkTest(unittest.TestCase):
    def testCheck(self):
        """
        """
        for t in test_data["racingKings"]["check"]:
            board = Board(t[0])
            expected = eval(t[1])
            
            self.assertEqual(checkMate(board), expected, "\nBoard representation:\n" + str(board) + "\nexpected:"+t[1])

# TODO: has to be implemented
class mainFunctionTest(unittest.TestCase):
    def testJumpStirdyStateCheck(self):
        pass
        
    def testJumpStirdyMoveCheck(self):
        pass
        
    def testRacingKingsMoveCheck(self):
        pass

    def testRacingKingsStateCheck(self):
        pass


if __name__ == '__main__':
    with open('test_data.json') as f:
        test_data = json.load(f)
        
    unittest.main()