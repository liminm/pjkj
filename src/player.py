from flask import Blueprint, request, Response
import json
from copy import deepcopy

from data import storage
import util


api = Blueprint('player', __name__)


# This endpoint is only for the frontend to verify tokens before saving them
@api.route('/playerlogin', methods = ['GET'])
def get_playerlogin():

	# Verify authorization
	playerID, response = util.auth(storage['players'], request)

	# If authentication fails, send error message and -code
	if not playerID:
		return Response(*response)

	return json.dumps({
		'id': playerID,
		'valid': True
	}, indent=4), 200


@api.route('/players', methods=['POST'])
def post_player():

	# Only teams are allowed to create players. Therefore, we authenticate with
	# a team token.
	teamID, response = util.auth(storage['teams'], request)

	# If authentication fails, send error message and -code
	if not teamID:
		return Response(*response)


	# Get the payload and parse it
	player = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

	# we can assign this player to a team based on the authenticated team
	player['team'] = teamID

	# Generate new id and token for this new player
	id = util.id()
	token = util.token()
	# TODO: Hash + Salt?
	player['token'] = token

	# Add the player to the database
	storage['players'][id] = player

	# DEBUG
	util.showDict(storage)

	return json.dumps({
		'id': id,
		'token': token
	}, indent=4), 201


@api.route('/players', methods=['GET'])
def get_players():

	# In order to not accidentally remove the tokens from the database, we copy
	# the entire dict here.
	players = deepcopy(storage['players'])

	# Remove tokens, since they're secrets :P
	for id in players:
		del players[id]['token']

	# Clients might only want a slice of the collection, which they can specify
	# using these URL parameters
	start = request.args.get('start', default = 0, type = int)
	count = request.args.get('count', default = None, type = int)

	players = util.paginate(players, start, count)

	return json.dumps(players, indent=4)


@api.route('/player/<id>', methods = ['GET'])
def get_player(id):

	if not id in storage['players']:
		return 'Error: Not found', 404

	# In order to not accidentally remove the tokens from the database, we copy
	# the entire dict here.
	player = deepcopy(storage['players'][id])

	# Remove token, since it's a secret :P
	del player['token']

	return json.dumps(player, indent=4)
