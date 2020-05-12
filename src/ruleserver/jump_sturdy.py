#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:47:31 2020

@author: vairee
"""
import bitboard
import numpy as np
from valid_move_check import ValidCheckJumpSturdy
#from WinConditions import checkwinRK




def fenStateCheck(state):
    """ 
    This will be only called at the beginning of a game and report if the enterd FEN string is valid
    FEN --> The FEN string wil be cheked for format and if there is at least two kings on the field
    history --> the gamedict for now until i know what we get/need  
    Returns a bool if it was valid and a String telling why it wasnt
    """
    

    #FEN = state['fen']
    FEN = state
        
    #check for valid FEN
    try:
        board = bitboard.Board(FEN)
    except: # syntax error on fen string
        return False, "SyntaxError", "FEN parsing error, seems to be invalid"
    """          
    #check for timebudget
    if (state['timeBudgets']['playerA'] <= 0) and (state['timeBudgets']['playerB'] <= 0):
        return False, "timeBudget", "Both players have no time left"
    
    if (state['timeBudgets']['playerA'] <= 0):
        return False, "timeBudget", "Player A has no time left"
    
    if (state['timeBudgets']['playerB'] <= 0):
        return False, "timeBudget", "Player B has no time left"
   """ 
    #TODO mittlere Rückgabe
    figs = board.board['wh'] | board.board['bl']
    print('{0:b}'.format(figs).zfill(64))
    test = '1000000100000000000000000000000000000000000000000000000010000001'
    print(test)
    print(str(board))
    #print('{0:b}'.format(figs & test).zfill(64))
    if all & test != 0:
        return False, None, "Figures in the corners"
    print(str(board))

    #TODO  check if the count of characters is valid
    pass
    """    
   # check if both kings are at the end of the board
    mask = np.int64(int("1"*8+"0"*8*7))
        
   # check if one of the kings won the game
    #if (board.board["k"] & board.board["wh"] & mask != 0):
       return True, "won", "white"
        
    if (board.board["k"] & board.board["bl"] & mask != 0):
       return True, "won", "black"
    """    
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
        
    # for check valid  movement
    try:
        if not moveCheck.check(FEN,uci):
            return False, None, "MoveError:Not a valid move!"
    except:
        return False, None, "InternalError:Internal Function is incorrect! Please report this error to the rule server team."
        
    # update hashmap
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

print(fenStateCheck("8/8/8/8/8/8/k7/8 w - - 0 1"))
           