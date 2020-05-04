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

    def __init__(self, FEN = None, Time = None):
        self.curBoard = ''
        self.lastBoard = ''
    
        self.lastPlayer = ''
        self.curPlayer = '' 
        self.maxTime = ''
        self.playerA = '' 
    
        start = "8/8/8/8/8/8/krbnKRBN/qrbnQRBN w - - 0 0"
        #redo this and put in fen state checkt and set up
        """
        self.board = bitboard.Board()
    
        if FEN == None :
            self.board.parse(start)
            self.lastBoard = self.board.board
            self.playerA = 'w'
            #self.lastplayer = 'bl'
        else :
            self.board.parse(FEN)
            self.lastBoard = self.board.board
            #TODO catch expection 
            self.lastplayer = self.board.scan(FEN)[8]
            self.playerA = self.board.scan(FEN)[8]
        """    
        if Time == None:
            self.maxTime = 30 
        else :
            self.maxTime = Time
        
    def setupTurn(self, FEN, history = None):
        """
        sets all parametrs for a Turn so the checks can go through 
        FEN is the FEN string
        history is the game dict
        """
        #catch exception
        parts = bitboard.Board.scan(FEN)
        self.curPlayer = parts[8]
        
        bitboard.Board.parse(FEN)
        self.curBoard = bitboard.Board.board

        if history != None:
            
            #Todo figure out how to access the fen
            bitboard.Board.parse(history['history'][-1]) #Todo check if newest turn is saved last or firat element
            self.lastPlayer   = history['history'][-1] #Todo figure out how to access the fen
            
            self.lastBoard = bitboard.Board.board

  
        
    def fenStateCheck(self,FEN):
        """ 
        to check if the starting conditions are allowing a game
        i.e. white doesnt win automatically
        """
        try:
        #check for valid FEN
        
        #check for timeoout
        pass
        #check for timebudget
        pass
        pass
    
    def move_check(self,uci,turnTime,history):
        r = ''
        state = ''
        winner = ''
        reason = {
                'U': "Invalid UCI string, values have to be between(inclusive) a-h and 1-8. with the format being i.e. e1g3",
                'M': "Could not move the figure in this way",
                'K': "Turn would put any king in checkmate"
                }
        
        valid = True
        
        # calling all the classes
        vmc = vm.ValidCheck()
        wc = rk_win.KingIsAttackedCheck
        
        #check for valid uci 
        if not self.validUCI(uci):
           r = 'U'
           valid = False
        #check for timeoout
        pass
        #check for timebudget
        pass
        #check if there is a figure
        pass
        #check if own figure moved
        pass
        # for check valid  movement
        pos = vmc.calc_positions(self.curBoard,self.lastBoard)
        if not vmc.check_valid_move(pos[0],pos[1][0],pos[1][1],pos[2][0],pos[2][1]) :
            valid = False
            r = 'M'
        #check for checkmate
        king = self.curBoard[self.curPlayer]&self.curBoard['k']
        moves = wc.calc_movesboard(wc.set_occupied_pos,)
        if not wc.king_is_attacked(king,wc.calc_movesboard()):
            valid = False
            r = 'K'
        #check for winning conditions
        pass
        FEN = self.board.__repr__(self.board)
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
        
        
    
   # todo exceptions bei scan, parse
rc = racingkings()
print(rc.validUCI(''))
#TODO Timemanagement
#TODO how to set starting player so player movement works out
#TODO exceptions for setup