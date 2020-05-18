from .ruleserver import racing_kings as rk
from .ruleserver import jump_sturdy as js

def stateCheck(type, state):

	if type == 'racingKings':
		return rk.fenStateCheck(state)

	elif type == 'jumpSturdy':
		return js.fenStateCheck(state)

	print("Fatal Error: unknown game")
	exit()


def moveCheck(type, moveEvent, state):

	if type == 'racingKings':
		return rk.moveCheck(moveEvent, state)

	elif type == 'jumpSturdy':
		return js.moveCheck(moveEvent, state)

	print("Fatal Error: unknown game")
	exit()
