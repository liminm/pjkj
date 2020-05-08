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

def fenStateCheck(state):
    
    return True, "", ""
    
def moveCheck(moveEvent,state):
    return True,gameState,"Alles Super!"
           