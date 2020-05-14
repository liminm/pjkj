from flask import request
import json
from copy import deepcopy

from __main__ import app, storage
import util


@app.route('/games', methods=['POST'])
def post_game():

	game = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

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
		del games[id]['settings']
		del games[id]['events']
		del games[id]['state']['fen']
		del games[id]['state']['timeBudgets']
		games[id]['playerNames'] = {
			'playerNameA': storage['players'][games[id]['players']['playerA']]['name'],
			'playerNameB': storage['players'][games[id]['players']['playerB']]['name']
		}
		del games[id]['players']

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

	return json.dumps(game, indent=4)
