#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:47:31 2020

@author: vairee
"""
import bitboard
#import valid_move_check as vm
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
        self.curPlayer = '' #TODO figure out how to set for the start turns so player check works
        self.maxTime = ''
    
        start = "8/8/8/8/8/8/krbnKRBN/qrbnQRBN w - - 0 0"
        
        board = bitboard.Board()
    
        if FEN == None :
            board.parse(start)
            self.lastBoard = board.board
            #self.lastplayer = 'b'
        else :
            board.parse(FEN)
            self.lastBoard = board.board
            self.lastplayer = board.scan(FEN)[8]
            
        if Time == None:
            self.maxTime = 30 #Todo valid iso 30 min format and get people to decide how long a game is max supoosed to be
        else :
            self.maxTime = Time
    
    def setupTurn(self, FEN, history = None):
        """
        sets all parametrs for a Turn so the checks can go through 
        FEN is the FEN string
        history is the game dict
        """
        parts = bitboard.Board.scan(FEN)
        self.curPlayer = parts[8]
        
        bitboard.Board.parse(FEN)
        self.curBoard = bitboard.Board.board

        if history != None:
            
            #Todo figure out how to access the fen
            bitboard.Board.parse(history['history'][-1]) #Todo check if newest turn is saved last or firat element
            self.lastPlayer   = history['history'][-1] #Todo figure out how to access the fen
            
            self.lastBoard = bitboard.Board.board

            
    def validation(self):
        #retB = True
        #retS = ''
        #check movement
        #pos = vm.ValidCheck.calc_positions()
        # if not vm.ValidCheck.check_valid_move(pos[0],pos[1][0],pos[1][1],pos[2][0],pos[2][1]) :
            #retB = False
           # retS = 'm'
        #check win conditon
        
        #return(retB,retS)
    
    