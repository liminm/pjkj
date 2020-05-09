#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:47:31 2020

@author: vairee
"""
import bitboard
import numpy as np
import valid_move_check as vm
from WinConditions import checkwinRK
from racing_kings_check_check import checkMate
#import test

def implication(a,b):
    return not a or b

class racingkings():
    """
    start is the FEN string, if it is none we wil start with the standart board and standart start player (white)
    Time is the max Time a gameis allowed to run
    the class has to be called once with the starting configueratioon before setting a turn 
    
    """

    def __init__(self, FEN = None, gameTime = None, turnTime = None):
    
        self.curPlayer = '' 
        self.turnTime = 60000
        self.playerA = ''
        
        self.board = bitboard.Board()
    
        self.start = "8/8/8/8/8/8/krbnKRBN/qrbnQRBN w - - 0 1"
        
        if not(gameTime == None):
            self.maxTime = gameTime
        if not(turnTime == None):
            self.turnTime = turnTime
       
        
            
        
    def setup(self, uci , history = None):
        """
        setups the Last and current boardstate, current board state is saved in self.board last board is save in self.lastBoard
        we also set current player
        """
        
        try:
            self.lastBoard = bitboard.Board(history)
            self.curPlayer = self.lastBoard.palyer
        except:
            return 'F'
        try:
            self.board.moveUCI(uci[:2],uci[2:4])
        except:
            return 'U'

    """
    things to check:
    - if at exactly 2 kings are on the field
    - if the number of carachters per type is valid
    - if the king is in chess
    - not both kings can be at the end of the field
    """
    def fenStateCheck(self,state):
        """ 
        This will be only called at the beginning of a game and report if the enterd FEN string is valid
        FEN --> The FEN string wil be cheked for format and if there is at least two kings on the field
        history --> the gamedict for now until i know what we get/need 
        
        Returns a bool if it was valid and a String telling why it wasnt
        """
        valid = True
        FEN = state['fen']
        con = None
        ret = None
        
        #check for valid FEN
        try:
            board = bitboard.Board(FEN)
        except error: # syntax error on fen string
            return False, "SyntaxError", ""
               
         #check for timebudget
        if (state['timeBudgets']['playerA'] <= 0) and (state['timeBudgets']['playerB'] <= 0):
            return False, "timeBudget", "Both players have no time left"
        if (state['timeBudgets']['playerA'] <= 0):
            return False, "timeBudget", "Player A has no time left"
        if (state['timeBudgets']['playerB'] <= 0):
            valid = False
            con = 'B'
            ret = 'timeBudget'
            return False, "timeBudget", "Player B has no time left"
        
        
        # with given data we cant check for timeout and do we need to do this ? 
        #check for timeout
        #if (self.turnTime - state['timeBudgets'][player]) <= 0:
            #valid = False
            #con = 'O'
            #ret  = 'timeOut'
        
            
        # check if the count of characters is valid
        #check if there are exactly two kings
        if len(board.findCharacter("k")) !=1 or len(board.findCharacter("K")) != 1:
            return False, "StateError", "There are not exactly 1 king on each side!"
        
        if not len(board.findCharacter("q")) in range(2) or not len(board.findCharacter("Q")) in range(2):
            return False, "StateError", "Each side has to have 0-2 queens!"
        
        if not len(board.findCharacter("n")) in range(2) or not len(board.findCharacter("N")) in range(2):
            return False, "StateError", "Each side has to have 0-2 knights!"
        
        if not len(board.findCharacter("b")) in range(2) or not len(board.findCharacter("B")) in range(2):
            return False, "StateError", "Each side has to have 0-2 bishops!"
        
        if not len(board.findCharacter("r")) in range(2) or not len(board.findCharacter("R")) in range(2):
            return False, "StateError", "Each side has to have 0-2 rooks!"
        
        if len(board.findCharacter("p")) !=0 or len(board.findCharacter("P")) != 0:
            return False, "StateError", "There are no pawns allowed in this game!"
        
        # TODO: check if the king is in chess
        
        
        # check if both kings are at the end of the board
        mask = np.int64(int("1"*8+"0"*8*7))
        
        # check if one of the kings won the game
        if (board.board["k"] & board.board["wh"] & mask != 0):
            return True, "won", "white"
        
        if (board.board["k"] & board.board["bl"] & mask != 0):
            return True, "won", "black"
        
        return True, "", ""
    
    def moveCheck(self,moveEvent,state):
        v,c,r = fenStateCheck(state)
        if not v:
            return False, None, c+":"+r
            
        
        # pick apart the input Data
        player = moveEvent[0]
        
        hashmap = state["boardHashMap"]
        event = moveEvent
        #set beginning variables
        r = None
        state,winner = None
        valid = True
        gameState = None
        
        #Set FEN for easier testing
        if type(state) == str:
             FEN = state
        elif type(state) == dict:
            FEN = state['fen']
        else:
            FEN = None
        
        try:
            board_before = bitboard.Board(FEN)
            board_after = bitboard.Board(FEN)
        except:
            return False, None, "SyntaxError:FEN String is invalid!"
            
        reason = {
                'U': "Invalid UCI string, values have to be between(inclusive) a-h and 1-8. with the format being i.e. e1g3",
                'M': "Could not move the figure in this way",
                'K': "Turn would put any king in checkmate",
                'H': "The old FEN String seems to be wrong",
                'V': None,
                'B': " The timebudget run out",
                'O': " You took to long for your turn"
                }
    
        # calling all the classes
        vmc = vm.ValidCheck()
        #wc = rk_win.KingIsAttackedCheck
        
        #check for valid uci
        uci = event["details"]
        try:
            board_after.movePlayer(uci)
        except:
            return False, None, "SyntaxError:UCI String is invalid!"
       
        ####### Setup the turns ######
        r = self.setup(moveEvent[1][0],FEN)
        if r is not None:
            valid = False
        
        #check for timebudget
        if (state['timeBudgets'][player]-moveEvent[1][1] ) <= 0:
            valid = False
            r = 'B'
            state = 'timeBudget'
            if player == 'playerA':
                winner = 'playerB'
            else:
                winner = 'playerA'
        else:
            state['timeBudgets'][player] = state['timeBudgets'][player]-moveEvent[1][1]
        
        #check for timeout
        if (self.turnTime - state['timeBudgets'][player]) <= 0:
            valid = False
            r = 'O'
            state = 'timeOut'
            if player == 'playerA':
                winner = 'playerB'
            else:
                winner = 'playerA'
                
         # for check valid  movement
        try:
            if not vmc.check(repr(self.lastBoard),repr(self.board)):
                return False, None, "MoveError:Not a valid move!"
        except:
            return False, None, "InternalError:Internal Function is incorrect! Please report this error to the rule server team."
            
        
        #check for checkmate
        king = self.curBoard[self.curPlayer]&self.board['k']
        moves = wc.calc_movesboard(wc.set_occupied_pos,)
        if checkMate(board_after):
            return False, None, "MoveError:The king is checked!"
        
        status = None
        # update hashmap
        if not board_after in hashmap:
            hashmap[board_after] = 1
        else:
            hashmap[board_after] +=1
        
        if hashmap[board_after] >= 3:
            winner, status = "draw"
        
        # everything is good
            
        # TODO: Wenn weiß gewinnt, hat schwarz noch ein zug
        if checkwinRK(board_after) and status is None:
            winner = if board_before.player=="w" : "playerA" else "playerB" # TODO: ask if playera is white or black
            status = "won"
        
        # checks if the white has already won before
        if checkwinRK(board_before) and board_before.player == "b" and status in [None, "won"]:
            if status == "won":
                winner, status = "draw"
            else:
                winner = "playerA"
                status = "won"
        
        if not status is None:
            #set the game state and other returns
            gameState = {
                    'type': status,
                    'winner': winner}
            moveEvent['details']['postFen'],state['FEN'] = repr(board_after)
            state['winner']  = winner
        
        
        
        return True,gameState,"Alles Super!"
           
          
    def validUCI(self,uci):
        ret = True
        if len(uci) == 4:
            for i in range(0,4):
                if (i== 0 or i == 2) and not(uci[i] in 'abcdefgh'):
                    ret = False
                    break
                if (i== 1 or i == 3) and not(uci[i] in '12345678'):
                    ret = False
                    break
        else :
            ret = False
        return ret

           
        
    


#TODO checkmate einbindung
#TODO exceptions bitbaord
#TODO check if valid move checks for own figure
#ToDo check if valid moves checks for any figure
