#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:47:31 2020

@author: vairee
"""
import bitboard
import valid_move_check as vm
#import racing_kings_check_check as rk_win
#import test

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
        
    def fenStateCheck(self,state):
        """ 
        This will be only called at the beginning of a game and report if the enterd FEN string is valid
        FEN --> The FEN string wil be cheked for format and if there is at least two kings on the field
        history --> the gamedict for now until i know what we get/need 
        
        Returns a bool if it was valid and a String telling why it wasnt
        """
        valid = True
        FEN = state['FEN']
        con = None
        ret = None
        
        #check for valid FEN
        try:
            parts = bitboard.Board.scan(FEN)
        except:
            con = 'F'
            valid = False
               
         #check for timebudget
        if (state['timeBudgets']['playerA'] <= 0) or (state['timeBudgets']['playerB'] <= 0):
            valid = False
            con = 'B'
            ret = 'timeBudget'
        
        
        # with given data we cant check for timeout and do we need to do this ? 
        #check for timeout
        #if (self.turnTime - state['timeBudgets'][player]) <= 0:
            #valid = False
            #con = 'O'
            #ret  = 'timeOut'
            
               
        # check for empty field
        if "8/8/8/8/8/8/8/8" in FEN :
            con = 'E'
            valid = False
            
        #check if there are at least two kings
        pass
        
        if con == None:
            self.playerA = parts[9]
            
        return (valid, ret)
    
    def moveCheck(self,moveEvent,state) :
        # pick apart the input Data
        player = moveEvent[0]
        
        
        #set beginning variables
        r = None
        state,winner = None
        valid = True 
        gameState = None
        
        
        #Set FEN for easier testing
        if type(state) == str :
             FEN = state
        elif type(state) == dict:
            FEN = state['FEN']
        else:
            FEN = None
    
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
        if not self.validUCI(moveEvent[1][0]):
           r = 'U'
           valid = False
           
        ####### Setup the turns ######
        r = self.setup(moveEvent[1][0],FEN)
        if r is not None : 
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
            if not vmc.check(repr(self.lastBoard),repr(self.board)) :
                valid = False
                r = 'M'
        except:
            valid = False
            r = 'H'
            
        
        #check for checkmate
        king = self.curBoard[self.curPlayer]&self.board['k']
        moves = wc.calc_movesboard(wc.set_occupied_pos,)
        if not wc.king_is_attacked(king,wc.calc_movesboard()):
            valid = False
            r = 'K'
        
        
        #check for winning conditions
        pass
    
        # everything is good
        
        if r is None :
        #TODO not quit right yet
            self.board.halfRounds += 1
        
            if self.curPlayer == self.playerA :
                self.board.roundCount += 1
                
            #set the game state and other returns
            gameState = {
                    'type': state,
                    'winner': winner}
            moveEvent['details']['postFen'],state['FEN'] = repr(self.board)
            state['winner']  = winner
        return (valid,gameState,reason[r])
           
          
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
