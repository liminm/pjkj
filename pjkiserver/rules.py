from .ruleserver import racing_kings as rk
from .ruleserver import jump_sturdy as js

def initialFEN(type):

	if type == 'racingKings':
		return rk.INITIAL_FEN

	elif type == 'jumpSturdy':
		return js.INITIAL_FEN

	return None

def stateCheck(type, state):

	if type == 'racingKings':
		return rk.fenStateCheck(state)

	elif type == 'jumpSturdy':
		return js.fenStateCheck(state)

	return False, None, ('Error: unknown game "' + type + '"')


def moveCheck(type, moveEvent, state):

	if type == 'racingKings':
		return rk.moveCheck(moveEvent, state)

	elif type == 'jumpSturdy':
		return js.moveCheck(moveEvent, state)

	return False, None, ('Error: unknown game "' + type + '"')
