import unittest
import json
import numpy as np

# test imports
from bitboard import Board
from valid_move_check import ValidCheck
from WinConditions import reihencheckrk
from WinConditions import reihencheckjs
from jump_sturdy import movePlayerJS
import jump_sturdy
import racing_kings
import racing_kings_check_check


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
        for i in range(len(test_data["racingKings"]["sampleGame"])-1):
            t = test_data["racingKings"]["sampleGame"][i]
            expected = test_data["racingKings"]["sampleGame"][i+1][0]
            board_moved = Board(t[0])
            uci = t[1] + t[2]
            board_moved.movePlayer(uci)
            
            message ="\nboard before move:\n" + str(Board(t[0])) + "\nactual board representation:\n" + str(board_moved) + "\nexpected board representation:\n"+ str(Board(expected)) + "\nmove:"+uci
            self.assertEqual(repr(board_moved), expected, message)
    
    def testMovePlayerJSValidness(self):
        for i in range(len(test_data["jumpStirdy"]["sampleGame"])-1):
            t = test_data["jumpStirdy"]["sampleGame"][i]
            after = test_data["jumpStirdy"]["sampleGame"][i+1]
            board = Board(t[0])
            board_moved = Board(after[0])
            uci = t[1] + t[2]
            character = board.getField(t[1])
            try:
                movePlayerJS(board, uci)
            except:
                self.assertTrue(False, "\nBoard throwed an exception!\nactual board representation:\n" + str(board) + "\nexpected board representation:\n"+ str(board_moved) + "\nmove:"+t[1]+t[2]+"\ncharacter:"+character+"\nboard:"+b)
                
            for b in board.board:
                message ="\nboard before move:\n" + str(Board(t[0])) + "\nactual board representation:\n" + str(board) + "\nexpected board representation:\n"+ str(board_moved) + "\nmove:"+t[1]+t[2]+"\ncharacter:"+character+"\nboard:"+b
                self.assertEqual(board.board[b], board_moved.board[b], message)
            

class MoveCheckTest(unittest.TestCase):
    
    def testMoveCheckRacingKings(self):
        """
        t[0] == fen string für board vor moveCheck
        t[1] == move in uci mit space separated
        t[2] == says if the move should be valid
        """
        v = ValidCheck()
        for t in test_data["racingKings"]["moveCheck"]+test_data["racingKings"]["sampleGameMoveCheck"]+test_data["racingKings"]["sampleGame"]:
            board = Board(t[0])
            board_moved = Board(t[0])
            moves = (t[1], t[2])
            exp = eval(t[3])
            character = None
            if exp:
                board_moved.movePlayer(moves[0], moves[1])
                character = board.getField(moves[0])
                
            is_valid, reason = v.check(repr(board), repr(board_moved))
            message = "\nReason: " + reason + "\nBoard representation before move:\n" + str(board) + "\nboard representation after move:\n"+ str(board_moved) + "\nmove:"+str(moves)+"\ncharacter:"+str(character)+"\nvalid:"+t[3]
            
            if len(t) > 4:
                message += "\ntestMessage:" + t[4]
            
            self.assertEqual(is_valid, exp, message)
            
    
    def testMoveCheckJumpStirdy(self):
        v = ValidCheck()
        for t in test_data["jumpStirdy"]["moveCheck"] + test_data["jumpStirdy"]["sampleGame"]:
            board = Board(t[0])
            board_moved = Board(t[0])
            uci = t[1] + t[2]
            exp = eval(t[3])
            try:
                if exp:
                    movePlayerJS(board_moved, uci)
            except:
                pass
            character = board.getField(t[1])
            is_valid, reason = v.check(repr(board), uci, "JS")
            self.assertEqual(is_valid, exp, "\nReason: " + reason + "\nBoard representation before move:\n" + str(board) + "\nboard representation after move:\n"+ str(board_moved) + "\nmove:"+t[1]+t[2]+"\ncharacter:"+character+"\nvalid:"+t[3])

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
            
            # TODO: make it run the check mate function and implement some more tests
            self.assertEqual(racing_kings_check_check.checkmate(board), expected, "\nBoard representation:\n" + str(board) + "\nexpected:"+t[1])

class JumpSturdyMainFunction(unittest.TestCase):
    def testJumpStirdyStateCheck(self):
        for t in test_data["jumpStirdy"]["mainFunction"] + test_data["jumpStirdy"]["sampleGame"]:
            expected = (eval(t[3]), eval(t[4]))
            if not expected[0]:
                continue
                
            uci = t[1] + t[2]
            try:
                board = Board(t[0])
            except SyntaxError:
                board = None
            state = {"fen":t[0]}
            
            jump_sturdy.movePlayerJS(board, uci)
            
            r = jump_sturdy.fenStateCheck(state)
            actual = (r[0], r[1])
                    
            #self.assertEqual(actual, expected, "\nBoard representation:\n" + str(board) + "\nmessage:"+r[2])
        
    def testJumpStirdyMoveCheck(self):
        for t in test_data["jumpStirdy"]["mainFunction"] + test_data["jumpStirdy"]["sampleGame"]:
            try:
                board = Board(t[0])
                board_moved = Board(t[0])
                moveEvent = {"type":"move",
                        "player":"playerA" if board.player == "wh" else "playerB",
                       "details": {"move":t[1]+t[2]}}
            except SyntaxError:
                moveEvent = {"type":"move",
                        "player":"playerA",
                       "details": {"move":t[1]+t[2]}}
                board = None
                
            state = {"fen":t[0], "boardHashMap":{}}
            
            uci = t[1] + t[2]
                
            exp = eval(t[3])
            expected = (exp, eval(t[4]))
            if exp:
                jump_sturdy.movePlayerJS(board_moved, uci)
            character = board.getField(t[1])
            
            r = jump_sturdy.moveCheck(moveEvent, state)
            actual = (r[0], r[1])
                    
            self.assertEqual(actual, expected, "\nBoard representation before move:\n" + str(board) + "\nBoard representationa after move:\n" + str(board_moved) + "\nmessage:"+r[2] + "\nmove:"+ uci)
      

class RacingKingsMainFunction(unittest.TestCase):    
    def testRacingKingsStateCheck(self):
        for t in test_data["racingKings"]["mainFunction"]+ test_data["racingKings"]["sampleGame"]:
            expected = (eval(t[3]), eval(t[4]))
            if not expected[0]:
                continue
                
            uci = t[1]+t[2]
            try:
                board = Board(t[0])
            except SyntaxError:
                board = None
            
            board.movePlayer(uci)
                
            state = {"fen":repr(board)}
                
            r = racing_kings.fenStateCheck(state)
            actual = (r[0], r[1])
                 
            #self.assertEqual(actual, expected, "\nBoard representation:\n" + str(board) + "\nmessage:"+r[2])
        
    def testRacingKingsMoveCheck(self):
        for t in test_data["racingKings"]["mainFunction"]+test_data["racingKings"]["sampleGame"]:
            expected = (eval(t[3]), eval(t[4]))
            try:
                board = Board(t[0])
                board_moved = Board(t[0])
                moveEvent = {"type":"move",
                        "player":"playerA" if board.player == "wh" else "playerB",
                       "details": {"move":t[1]+t[2]}}
            except SyntaxError:
                moveEvent = {"type":"move",
                        "player":"playerA",
                       "details": {"move":t[1]+t[2]}}
                board = None
            state = {"fen":t[0], "boardHashMap":{}}
            uci = t[1] + t[2]
                
            exp = eval(t[3])
            expected = (exp, eval(t[4]))
            if exp:
                board_moved.movePlayer(uci)
            character = board.getField(t[1])
                    
            r = racing_kings.moveCheck(moveEvent, state)
            actual = (r[0], r[1])
                    
            self.assertEqual(actual, expected, "\nBoard representation before move:\n" + str(board) + "\nBoard representationa after move:\n" + str(board_moved) + "\nmessage:"+r[2] + "\nmove:"+ uci+ "\nfen:"+repr(board))


if __name__ == '__main__':
    with open('test_data.json') as f:
        test_data = json.load(f)
        
    unittest.main()