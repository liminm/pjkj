import os

os.chdir("..")
print(os.getdir())

from ruleserver.bitboard import Board
from ruleserver.valid_move_check import ValidCheck
from ruleserver.WinConditions import reihencheckrk
from ruleserver.WinConditions import reihencheckjs
from ruleserver.jump_sturdy import movePlayerJS
from ruleserver import jump_sturdy
from ruleserver import racing_kings
from ruleserver import racing_kings_check_check