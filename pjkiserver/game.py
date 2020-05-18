from flask import Blueprint, request
import json
from copy import deepcopy

from .data import storage
from . import rules, util


api = Blueprint('game', __name__)


@api.route('/games', methods=['POST'])
def post_game():

	# Get the payload and parse it
	game = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

	# Make sure that a player can't play against itself
	# This is not allowed because we need to be able to uniquely map
	# PlayerID -> Player to identify who is making a move, which isn't possible
	# if both players have the same ID.
	if game['players']['playerA'] == game['players']['playerB']:
		return "Error: player can't play against itself", 409

	# Initialize the game state according to the database layout
	# (See https://gitlab.tubit.tu-berlin.de/PJ-KI/server/snippets/631)
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
	# Make sure the timeout is an int and not a string
	game['settings']['timeout'] = int(game['settings']['timeout'])
	# Initialize eventstream
	game['events'] = []

	# Check initial state with Ruleserver
	#valid, gameEnd, reason = rules.stateCheck(game['type'], game['state'])
	#if not valid:
	#	return 'Error: Game state invalid\nReason:' + reason, 400
	#if gameEnd:
	#	return 'Error: Game already ended\ngameEnd:' + gameEnd, 409

	# Generate a new id for this game
	id = util.id()

	# Add it to the database
	storage['games'][id] = game

	# DEBUG
	util.showDict(storage)

	return json.dumps({
		'id': id
	}, indent=4), 201


@api.route('/games', methods=['GET'])
def get_games():

	# In order to not accidentally remove data from the database, we copy
	# the entire dict here.
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

	# Clients might only want a slice of the collection, which they can specify
	# using these URL parameters. They can also filter by state.
	start = request.args.get('start', default = 0, type = int)
	count = request.args.get('count', default = None, type = int)
	state = request.args.get('state', default = '*', type = str)

	games = util.paginate(games, start, count)
	games = util.filterState(games, state)

	return json.dumps(games, indent=4)


@api.route('/game/<id>', methods = ['GET'])
def get_game(id):

	if not id in storage['games']:
		return 'Error: Not found', 404

	# In order to not accidentally remove data from the database, we copy
	# the entire dict here.
	game = deepcopy(storage['games'][id])

	# Remove stuff not needed for clients here
	del game['events']
	del game['state']['boardHashMap']

	# Get the names of the players
	playerNameA = storage['players'][game['players']['playerA']]['name']
	playerNameB = storage['players'][game['players']['playerB']]['name']

	# Provide the player IDs as well as the names, because frontend wanted it
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
