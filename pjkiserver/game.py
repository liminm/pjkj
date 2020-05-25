from flask import Blueprint, request, Response
import json
from copy import deepcopy

from .storage.storage import storage
from . import schemas, rules, util


api = Blueprint('game', __name__)


@api.route('/games', methods=['POST'])
def post_game():

	# Parse and validate payload
	game, error = schemas.parseAndCheck(request.data, schemas.game)
	if error:
		return Response(*error)

	# We're gonna need these a bunch
	playerA = game['players']['playerA']
	playerB = game['players']['playerB']

	# Make sure the mentioned players actually exist
	if not playerA in storage['players']:
		return "Error: Player {} does not exist".format(playerA), 409
	if not playerB in storage['players']:
		return "Error: Player {} does not exist".format(playerB), 409

	# Make sure that a player can't play against itself
	# This is not allowed because we need to be able to uniquely map
	# PlayerID -> Player to identify who is making a move, which isn't possible
	# if both players have the same ID.
	if playerA == playerB:
		return "Error: Player can't play against itself", 409

	# Make sure only teams actually playing this game type can participate
	teamA = storage['players'][playerA]['team']
	teamB = storage['players'][playerB]['team']
	if storage['teams'][teamA]['type'] != game['type']:
		return "Error: Team {} can't play {}".format(teamA, game['type']), 409
	if storage['teams'][teamB]['type'] != game['type']:
		return "Error: Team {} can't play {}".format(teamB, game['type']), 409

	# If no initial FEN string is given, we get the defaults from the rules
	initialFEN = game['settings'].get('initialFEN') or rules.initialFEN(game['type'])

	# Initialize the game state according to the database layout
	# (See https://gitlab.tubit.tu-berlin.de/PJ-KI/server/snippets/631)
	game['state'] = {
		'state': 'planned',
		'winner': None,
		'fen': initialFEN,
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
	valid, gameEnd, reason = rules.stateCheck(game['type'], game['state'])
	if not valid:
		return 'Error: Game state invalid\nReason:' + reason, 400
	if gameEnd:
		return 'Error: Game already ended\ngameEnd:' + gameEnd, 409

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

	# Clients might only want a slice of the collection, which they can specify
	# using these URL parameters. They can also filter by state.
	start = request.args.get('start', default = 0, type = int)
	count = request.args.get('count', default = None, type = int)
	state = request.args.get('state', default = '*', type = str)

	# In order to not accidentally remove data from the database, we copy
	# the entire dict here.
	games = deepcopy(storage['games'])

	# Apply filter
	games = util.filterState(games, state)

	# Take length after filter but before pagination to get number of games
	# with this filter
	totalCount = len(games)

	# Apply pagination
	games = util.paginate(games, start, count)

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

	return json.dumps({
		'totalCount': totalCount,
		'items': games
	}, indent=4)


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
