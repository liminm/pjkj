#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:47:31 2020

@author: vairee
"""
import bitboard
import numpy as np
import valid_move_check as vm
from WinConditions import reihencheckrk
from racing_kings_check_check import checkMate

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
        return False, None, "SyntaxError:The FEN String is invalid!"

    #check for timebudget
    if (state['timeBudgets']['playerA'] <= 0) and (state['timeBudgets']['playerB'] <= 0):
        return False, None, "timeBudget:Both players have no time left"
    if (state['timeBudgets']['playerA'] <= 0):
        return False, None, "timeBudget:Player A has no time left"
    if (state['timeBudgets']['playerB'] <= 0):
        return False, None, "timeBudget:Player B has no time left"

    # check if the count of characters is valid
    if len(board.findCharacter("k")) !=1 or len(board.findCharacter("K")) != 1:
        return False, None, "StateError:There are not exactly 1 king on each side!"

    if not len(board.findCharacter("q")) in range(2) or not len(board.findCharacter("Q")) in range(2):
        return False, None, "StateError:Each side has to have 0-2 queens!"

    if not len(board.findCharacter("n")) in range(2) or not len(board.findCharacter("N")) in range(2):
        return False, None, "StateError:Each side has to have 0-2 knights!"

    if not len(board.findCharacter("b")) in range(2) or not len(board.findCharacter("B")) in range(2):
        return False, None, "StateError:Each side has to have 0-2 bishops!"

    if not len(board.findCharacter("r")) in range(2) or not len(board.findCharacter("R")) in range(2):
        return False, None, "StateError:Each side has to have 0-2 rooks!"

    if len(board.findCharacter("p")) !=0 or len(board.findCharacter("P")) != 0:
        return False, None, "StateError:There are no pawns allowed in this game!"

        
    if checkMate(board):
        return False, None, "StateError:King can not be in check!"


    # 50 moves rule
    if (board.halfRounds >= 50):
        return True, {"type":"50Move", "winner":"draw"}, ""

    # check if both kings are at the end of the board
    mask = np.int64(int("1"*8+"0"*8*7))

    # check if one of the kings won the game
    if ((board.board["k"] & board.board["wh"] & mask != 0) and (board.board["k"] & board.board["bl"] & mask != 0)):
        return True, {"type":"draw", "winner":"draw"}, ""

    if (board.board["k"] & board.board["wh"] & mask != 0):
        return True, {"type": "win", "winner":"PlayerA"}, ""

    if (board.board["k"] & board.board["bl"] & mask != 0):
        return True, {"type": "win", "winner":"PlayerB"}, ""

    return True, None, "Alles Super!"

def moveCheck(self,moveEvent,state):
    #--------------------------Setup-----------------------
    #set beginning variables
    r = None
    status,winner = None
    valid = True
    gameState = None
    player = moveEvent[0]
    hashmap = state["boardHashMap"]
    event = moveEvent

    vmc = vm.ValidCheck()

    #for testing
    if type(state) == str:
        FEN = state
    elif type(state) == dict:
        FEN = state['fen']

    #------------------------ validity testing--------------
    #checkfor valid FEN
    v,c,r = fenStateCheck(state)
    if not v:
        return False, None,r

    #TODO state ?
    #check for timebudget
    if (state['timeBudgets'][player]-moveEvent[1][1] ) <= 0:
        valid = False
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

        #create boards
        try:
            board_before = bitboard.Board(FEN)
            board_after = bitboard.Board(FEN)
        except:
            return False, None, "SyntaxError:FEN String is invalid!"


        #try the move
        uci = event["details"]['uci']
        try:
            board_after.movePlayer(uci)
        except:
            return False, None, "SyntaxError:UCI String is invalid!"


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

        # update hashmap
        if not board_after in hashmap:
            hashmap[board_after] = 1
        else:
            hashmap[board_after] +=1

        if hashmap[board_after] >= 3:
            winner, status = "draw"

        # everything is good
            
        if checkwinRK(board_after) and status is None:
            winner = if board_before.player=="w" : "playerA" else "playerB" # TODO: ask if playera is white or black
            status = "won"

        # checks if the white has already won before
        if reihencheckrk(board_before) and board_before.player == "b" and status in [None, "won"]:
            if status == "won":
                winner, status = "draw"
            else:
                winner = "playerA"
                status = "won"

        if not (status is None):
            #set the game state and other returns
            gameState = {
                    'type': status,
                    'winner': winner}
            moveEvent['details']['postFen'],state['FEN'] = repr(board_after)
            state['winner']  = winner

        return True,gameState,"Alles Super!"

