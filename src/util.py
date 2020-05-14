import string
import random
import json

id_len = 16
token_len = 42

def randomString(n):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def id():
	return randomString(id_len)

def token():
	return randomString(token_len)

def showDict(dict):
	print('\033c')
	print(json.dumps(dict, indent=4))

def checkAuth(dict, token):
	for id in dict:
		if dict[id]['token'] == token:
			return id

	return None

def opponent(player):
	if player == 'playerA':
		return 'playerB'
	elif player == 'playerB':
		return 'playerA'

	return None

def playerFromID(players, id):
	return list(players.keys())[ list(players.values()).index(id) ]

def paginate(listDict, start, count):
	dictList = list(listDict.items())
	end = start + count if count else None
	truncList = dictList[start:end]
	return dict(truncList)

def filterState(listDict, state):
	if (state == '*'):
		return listDict

	dictList = list(listDict.items())
	filteredList = list(
		filter(lambda el: el[1]['state']['state'] == state, dictList))
	return dict(filteredList)
