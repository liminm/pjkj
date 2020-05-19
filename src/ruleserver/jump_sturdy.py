#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:47:31 2020

@author: vairee
"""
import numpy as np
import re

from .bitboard import Board
from .valid_move_check import ValidCheckJumpSturdy
from .WinConditions import reihencheckjs

INITIAL_FEN = "1bbbbbb1/1bbbbbb1/8/8/8/8/1BBBBBB1/1BBBBBB1 w - - 0 1"

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
        board = Board(FEN)
    except: # syntax error on fen string
        return False,None ,"SyntaxError :FEN parsing error, seems to be invalid"

    #check for invalid figures
    if "r" in FEN :
         return False,None,"SyntaxError :FEN parsing error, no rooks allowed in jump sturdy"

    if "n" in FEN :
        return False,None ,"SyntaxError :FEN parsing error, no knights allowed in jump sturdy"

    if "p" in FEN :
        return False,None ,"SyntaxError :FEN parsing error, no pawns allowed in jump sturdy"

    # Check for four corners
    figs = board.board['wh'] | board.board['bl']
    mask = 0b1000000100000000000000000000000000000000000000000000000010000001
    if (figs & mask) > 0:
        return False, None, "StateError:Figures in the corners"

    #check if the count of characters is valid
    if (not len(board.findCharacter("B")) in range(13)) or (not len(board.findCharacter("b")) in range(13)):
            return False, None,"StateError: Each side has to have 0-12 singles!"

    if not len(board.findCharacter("K")) in range(7) or not len(board.findCharacter("k")) in range(7):
            return False,None ,"StateError: Each side has to have 0-6 monocoloured doubles!"

    if not len(board.findCharacter("Q")) + len(board.findCharacter("q")) in range(13):
            return False,None ,"StateError: there can only be 0-12 doubles!"

    if not (len(board.findCharacter("Q")) + len(board.findCharacter("q")) + len(board.findCharacter("B")) + len(board.findCharacter("b")) + len(board.findCharacter("K")) + len(board.findCharacter("k")))in range(25):
            return False,None ,"StateError : there can only be 0-24 figures on the board at any time!"

    #check for win
    if reihencheckjs(board,board.player) :
       if board.player == 'w' :
           return True,{'type' : "win", 'winner' : "playerA"},""
       else :
           return True,{'type' : "win", 'winner' : "playerB"},""

    return True,None, ""

def moveCheck(moveEvent,state):
    #set beginning variables
    hashmap = state["boardHashMap"]
    event = moveEvent
    player = moveEvent["player"]
    status = None
    winner = None
    valid = True
    gameState = None

    # calling all the classes
    moveCheck =  ValidCheckJumpSturdy()

    #check for valid FEN
    v,c,r = fenStateCheck(state)
    if not v:
        return False, None,r

    #Set FEN for easier testing
    if type(state) == str:
        FEN = state
    elif type(state) == dict:
        FEN = state['fen']

    #create Boards
    try:
        board_before = Board(FEN)
        board_after = Board(FEN)
    except:
        return False, None, "SyntaxError:FEN String is invalid!  "

    uci = event["details"]['move']

    #for check valid  movement
    try:
        valid_move, reason = moveCheck.check(FEN,uci)
        if not valid_move:
            return False, None, "MoveError:" + reason + "!"
    except:
        return False, None, "InternalError:Internal Function is incorrect! Please report this error to the rule server team."

    #Try the move
    try:
        movePlayerJS(board_after, uci)
    except:
        return False, None, "SyntaxError:UCI String is invalid!"


    #check for win
    if reihencheckjs(board_after,board_after.player) :
        if board_after.player == 'w' :
            return True,{'type' : "win", 'winner' : "playerA"},""
        else :
            return True,{'type' : "win", 'winner' : "playerB"},""


    #update hashmap
    if not board_after in hashmap:
        hashmap[board_after] = 1
    else:
        hashmap[board_after] +=1
        if hashmap[board_after] >= 3:
            winner = status = "draw"

    #set the game state and other returns
    if not status is None:
         gameState = {
                 'type': status,
                 'winner': winner}
         moveEvent['details']['postFen'],state['FEN'] = repr(board_after)
         state['winner']  = winner

    return valid,gameState,"Alles Super!"

def movePlayerJS(self, start, end=None, logging=False):
    if end is None:
        m = re.compile("([a-h][1-8])[- ]?([a-h][1-8])").match(start)
        if m is None:
            raise SyntaxError("Syntax Error in UCI String!")

        start = m.group(1)
        end = m.group(2)

    if logging:
        move = [repr(self), start, end, "True"]

    # halbzüge
    newRound = self.halfRounds
    startField = self.getField(start)
    endField = self.getField(end)
    startFieldOwner = self.getOwner(start)
    endFieldOwner = self.getOwner(end)

    # handling end field
    if startFieldOwner == endFieldOwner and endField.lower() == "b": # jumping on own character
        self.setField(end, "k" if startField.lower() == startField else "K")
    elif endField is None: # jumping on empty field
        self.setField(end, "b" if startField.lower() == startField else "B")
    elif startFieldOwner != endFieldOwner: # attacking enemy
        newRound = -1
        if endField.lower() == "q":
            self.setField(end, "k" if startField.lower() == startField else "K")
        elif endField.lower() == "k":
            self.setField(end, "q" if startField.lower() == startField else "Q")
        else:
            self.setField(end, "b" if startField.lower() == startField else "B")
    else:
        raise ValueError("")

    # handling start field
    if startField.lower() == "b":
        self.removeField(start)
    elif startField.lower() == "q":
        self.setField(start, "B" if startField.lower() == startField else "b")
    elif startField.lower() == "k":
        self.setField(start, "b" if startField.lower() == startField else "B")

    if self.player == "b":
        self.roundCount+=1
    if self.player == "w":
        self.player = "b"
    else:
        self.player = "w"

    if logging:
        self.log.append(move)
    self.halfRounds = newRound+1
