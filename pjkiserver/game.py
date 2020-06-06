from flask import Blueprint, request, Response
import json
from copy import deepcopy

from .storage.storage import storage, syncDB
from . import schemas, rules, util


api = Blueprint('game', __name__)


@api.route('/games', methods=['POST'])
def post_game():

	# Parse and validate payload
	game, error = schemas.parseAndCheck(request.data, schemas.game)
	if error:
		return Response(*error)

	# Stuff we have to do for both players goes here
	for player in game['players']:

		# We're gonna need this a bunch
		playerID = game['players'][player]['id']

		# Make sure the mentioned players actually exist
		if not playerID in storage['players']:
			return "Error: Player {} does not exist".format(playerID), 409

		# Make sure only teams actually playing this game type can participate
		team = storage['players'][playerID]['team']
		if storage['teams'][team]['type'] != game['type']:
			return "Error: Team {} can't play {}".format(team, game['type']), 409

		# Initialize time budgets
		game['players'][player]['timeBudget'] = game['players'][player]['initialTimeBudget']

	# Make sure that a player can't play against itself
	# This is not allowed because we need to be able to uniquely map
	# PlayerID -> Player to identify who is making a move, which isn't possible
	# if both players have the same ID.
	if game['players']['playerA']['id'] == game['players']['playerB']['id']:
		return "Error: Player can't play against itself", 409

	# If no initial FEN string is given, we get the defaults from the rules
	initialFEN = game['settings'].get('initialFEN') or rules.initialFEN(game['type'])

	# Initialize the game state according to the database layout
	# (See https://gitlab.tubit.tu-berlin.de/PJ-KI/server/snippets/631)
	game['state'] = {
		'state': 'planned',
		'winner': None,
		'fen': initialFEN,
		'boardHashMap': {}
	}
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

	# Save changes to persistent DB
	syncDB(['games'])

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
		del game['state']['boardHashMap']
		for player in game['players']:
			playerID = game['players'][player]['id']
			game['players'][player] = {
				'name': storage['players'][playerID]['name']
			}

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

	# Add player names for frontend convenience
	for player in game['players']:
		playerID = game['players'][player]['id']
		game['players'][player]['name'] = storage['players'][playerID]['name']

	return json.dumps(game, indent=4)
