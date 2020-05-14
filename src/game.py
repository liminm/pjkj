from flask import request
import json
from copy import deepcopy

from __main__ import app, storage
import util


@app.route('/games', methods=['POST'])
def post_game():

	game = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

	if game['players']['playerA'] == game['players']['playerB']:
		return "Error: player can't play against itself", 409

	game['state'] = {
		'state': 'planned',
		'winner': None,
		'fen': game['settings']['initialFEN'],
		'timeBudgets': {
			'playerA': game['settings']['timeBudget'],
			'playerB': game['settings']['timeBudget']
		},
		'boardHashMap': {}
	}
	game['settings']['timeout'] = int(game['settings']['timeout'])
	game['events'] = []

	# TODO: Check initial state with Ruleserver
	#valid, reason = ruleServer.stateCheck(game['state'])
	#if not valid:
	#	return json.dumps(reason), 400

	id = util.id()

	storage['games'][id] = game

	# DEBUG
	util.showDict(storage)

	return json.dumps({
		'id': id
	}, indent=4), 201


@app.route('/games', methods=['GET'])
def get_games():

	games = deepcopy(storage['games'])

	# Remove stuff not needed in listing and add player names
	for id in games:
		game = games[id]
		del game['settings']
		del game['events']
		del game['state']['fen']
		del game['state']['timeBudgets']
		del game['state']['boardHashMap']
		game['playerNames'] = {
			'playerNameA': storage['players'][game['players']['playerA']]['name'],
			'playerNameB': storage['players'][game['players']['playerB']]['name']
		}
		del game['players']

	start = request.args.get('start', default = 0, type = int)
	count = request.args.get('count', default = None, type = int)
	state = request.args.get('state', default = '*', type = str)

	games = util.paginate(games, start, count)
	games = util.filterState(games, state)

	return json.dumps(games, indent=4)


@app.route('/game/<id>', methods = ['GET'])
def get_game(id):

	if not id in storage['games']:
		return 'Error: Not found', 404

	game = deepcopy(storage['games'][id])

	del game['events']
	del game['state']['boardHashMap']

	playerNameA = storage['players'][game['players']['playerA']]['name']
	playerNameB = storage['players'][game['players']['playerB']]['name']

	game['players'] = {
		'playerA': {
			'id': game['players']['playerA'],
			'name': playerNameA
		},
		'playerB': {
			'id': game['players']['playerB'],
			'name': playerNameB
		}
	}

	return json.dumps(game, indent=4)
