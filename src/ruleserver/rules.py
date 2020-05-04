#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:47:31 2020

@author: vairee
"""
import bitboard
import valid_move_check as vm
import racing_kings_check_check as rk_win
#import test

class racingkings():
    """
    start is the FEN string, if it is none we wil start with the standart board and standart start player (white)
    Time is the max Time a gameis allowed to run
    the class has to be called once with the starting configueratioon before setting a turn 
    
    """

    def __init__(self, FEN = None, gameTime = None, turnTime = None):
    
        self.curPlayer = '' 
        self.maxTime = 120000
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
        if type(history) == str :
            try:
                self.lastBoard = self.board.parse(history)
                parts = self.board.scan(history)
                self.curPlayer = parts[9]
            except:
                return "failed to parse the FEN"
        elif type(history) == dict:
            try:
                self.lastBoard = self.board.parse(history['history'][-1]['FEN'])
                parts = self.board.scan(history['history'][-1]['FEN'])
                self.curPlayer = parts[9]
            except:
                return "failed to parse the FEN"
        else:
                self.lastBoard = self.board.parse(self.start)
                parts = self.board.scan(self.start)
                self.curPlayer = parts[9]
        
        self.board.moveUCI(uci[:2],uci[2:4])
  
        
    def fenStateCheck(self,FEN, history):
        """ 
        This will be only called at the beginning of a game and report if the enterd FEN string is valid
        FEN --> The FEN string wil be cheked for format and if there is at least two kings on the field
        history --> the gamedict for now until i know what we get/need 
        
        Returns a bool if it was valid and a String telling why it wasnt
        """
        valid = True
        con = 'V'
        condition = {
                'F' : " The FEN String is not acaptable, to many/less fields or diffrent figures",
                'E': "We cant play on an Empty board need at least two kings",
                'V': None
                }
        
        #check for valid FEN
        try:
            parts = bitboard.Board.scan(FEN)
        except:
            con = 'F'
            valid = False
        #check for timeout
        pass
        #check for timebudget
        pass
        # check for empty field
        if "8/8/8/8/8/8/8/8" in FEN :
            con = 'E'
            valid = False
        #check if there are at least two kings
        if con == '':
            self.playerA = parts[9]
        return (valid, condition[con])
    
    def moveCheck(self,uci,turnTime,history):
        r = 'V'
        state = None
        winner = None
        valid = True
        if type(history) == str :
             FEN = history
        elif type(history) == dict:
            FEN = history['history'][-1]['FEN']
        else:
            FEN = ''
    
        reason = {
                'U': "Invalid UCI string, values have to be between(inclusive) a-h and 1-8. with the format being i.e. e1g3",
                'M': "Could not move the figure in this way",
                'K': "Turn would put any king in checkmate",
                'H': "The old FEN String seems to be wrong",
                'V': None    
                }
    
        # calling all the classes
        vmc = vm.ValidCheck()
        wc = rk_win.KingIsAttackedCheck
        #check for valid uci
        if not self.validUCI(uci):
           r = 'U'
           valid = False
           
        ####### Setup the turns ######
        if self.setup(uci,history) != None:
            valid = False
            r = 'H'
        
        #check for timeoout
        pass
        #check for timebudget
        pass
        #check if there is a figure
        pass
        #check if opponents figure moved
        pass
        """
        # for check valid  movement
        pos = vmc.calc_positions(self.board,self.lastBoard)
        if not vmc.check_valid_move(pos[0],pos[1][0],pos[1][1],pos[2][0],pos[2][1]) :
            valid = False
            r = 'M'
        #check for checkmate
        king = self.curBoard[self.curPlayer]&self.board['k']
        moves = wc.calc_movesboard(wc.set_occupied_pos,)
        if not wc.king_is_attacked(king,wc.calc_movesboard()):
            valid = False
            r = 'K'
        """
        #check for winning conditions
        pass
        # everything is good
        if r == 'V':
            self.board.halfRounds = 1
            if self.curPlayer == self.playerA :
                self.board.roundCount += 1
                FEN = repr(self.board)
        
        return (valid,FEN,state,winner,reason[r])
           
          
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
        
        
    

rc = racingkings()
print(rc.moveCheck('e7e8',1,"8/8/8/8/8/8/krbnKRBN/qrbnQRBN w - - 0 1"))
#TODO Timemanagement
#TODO how to set starting player so player movement works out
#TODO exceptions bitbaord
#TODO round counts increment 
