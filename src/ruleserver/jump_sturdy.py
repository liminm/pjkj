#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:47:31 2020

@author: vairee
"""
import bitboard
import numpy as np
from valid_move_check import ValidCheckJumpSturdy
from WinConditions import reihencheckjs




def fenStateCheck(state):
    """ 
    This will be only called at the beginning of a game and report if the enterd FEN string is valid
    FEN --> The FEN string wil be cheked for format and if there is at least two kings on the field
    history --> the gamedict for now until i know what we get/need  
    Returns a bool if it was valid and a String telling why it wasnt
    """
    

    #Set FEN for easier testing
    if type(state) == str:
        FEN = state
    elif type(state) == dict:
        FEN = state['fen']
        
    #check for valid FEN
    try:
        board = bitboard.Board(FEN)
    except: # syntax error on fen string
        return False,None ,"SyntaxError :FEN parsing error, seems to be invalid"
    
    #check for invalid figures
    if "r" in FEN :
         return False,None,"SyntaxError :FEN parsing error, no rooks allowed in jump sturdy"
     
    if "k" in FEN :
        return False,None ,"SyntaxError :FEN parsing error, no knights allowed in jump sturdy"
    
    if "p" in FEN :
        return False,None ,"SyntaxError :FEN parsing error, no pawns allowed in jump sturdy"
    
    """          
    #check for timebudget
    if (state['timeBudgets']['playerA'] <= 0) and (state['timeBudgets']['playerB'] <= 0):
        return False,timeBudget ,"timeBudget : Both players have no time left"
    
    if (state['timeBudgets']['playerA'] <= 0):
        return False,timeBudget ,"timeBudget : Player A has no time left"
    
    if (state['timeBudgets']['playerB'] <= 0):
        return False,timeBudget ,"timeBudget : Player B has no time left"
   """ 
   
    # Check for four corners
    figs = board.board['wh'] | board.board['bl']
    mask = 0b1000000100000000000000000000000000000000000000000000000010000001
    if (figs & mask) > 0:
        return False, None, "StateError:Figures in the corners"

    #check if the count of characters is valid
    if not len(board.findCharacter("B")) in range(12) or not len(board.findCharacter("b")) in range(12):
            return False, None,"StateError: Each side has to have 0-12 singles!"
    
    if not len(board.findCharacter("K")) in range(6) or not len(board.findCharacter("k")) in range(6):
            return False,None ,"StateError: Each side has to have 0-6 monocoloured doubles!"
    
    if not len(board.findCharacter("Q")) + len(board.findCharacter("q")) in range(12):
            return False,None ,"StateError: there can only be 0-12 doubles!"
        
    if not (len(board.findCharacter("Q")) + len(board.findCharacter("q")) + len(board.findCharacter("B")) + len(board.findCharacter("b")) + len(board.findCharacter("K")) + len(board.findCharacter("k")))in range(24):
            return False,None ,"StateError : there can only be 0-24 figures on the board at any time!"
    
    #check for win
    if reihencheckjs(board,board.player) :
        pass
        #TODO set winner 
         
    return True, "", ""

    
def moveCheck(moveEvent,state):
    #set beginning variables
    hashmap = state["boardHashMap"]
    event = moveEvent
    player = moveEvent[0]
    status,winner = None
    valid = True
    gameState = None
        
    # calling all the classes
    moveCheck =  ValidCheckJumpSturdy()
        
    #check for valid FEN
    v,c,r = fenStateCheck(state)
    if not v:
        return False, None, c+":"+r
        
    #Set FEN for easier testing
    if type(state) == str:
        FEN = state
    elif type(state) == dict:
        FEN = state['fen']
            
    #check for timebudget
    if (state['timeBudgets'][player]-moveEvent[1][1] ) <= 0:
        valid = False
        status = 'timeBudget'
        if player == 'playerA':
            winner = 'playerB'
        else:
            winner = 'playerA'
    else:
        state['timeBudgets'][player] = state['timeBudgets'][player]-moveEvent[1][1]
        
   #check for timeout
    if(60000 - state['timeBudgets'][player]) <= 0:
       valid = False
       status = 'timeOut'
       if player == 'playerA':
           winner = 'playerB'
    else:
            winner = 'playerA'
                
    #create Boards
    try:
        board_before = bitboard.Board(FEN)
        board_after = bitboard.Board(FEN)
    except:
        return False, None, "SyntaxError:FEN String is invalid!  "
         
    #Try the move
    uci = event["details"]['uci']
    try:
        board_after.movePlayer(uci)
    except:
        return False, None, "SyntaxError:UCI String is invalid!"    
        
    #for check valid  movement
    try:
        if not moveCheck.check(FEN,uci):
            return False, None, "MoveError:Not a valid move!"
    except:
        return False, None, "InternalError:Internal Function is incorrect! Please report this error to the rule server team."
    
    #check for win
    if reihencheckjs(board,board.player) :
        pass
        #TODO set winner 
         
        
    #update hashmap
    if not board_after in hashmap:
        hashmap[board_after] = 1
    else:
        hashmap[board_after] +=1
        if hashmap[board_after] >= 3:
            winner, status = "draw"
            
    #set the game state and other returns
    if not status is None:
         gameState = {
                 'type': status,
                 'winner': winner}
         moveEvent['details']['postFen'],state['FEN'] = repr(board_after)
         state['winner']  = winner
    
    return valid,gameState,"Alles Super!"
