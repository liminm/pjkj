from flask import request, Response
import json
from copy import deepcopy

from __main__ import app, storage
import util


@app.route('/playerlogin', methods = ['GET'])
def get_playerlogin():

	authHeader = request.headers.get('Authorization')

	if not authHeader:
		return Response('Error: unauthorized', 401, {'WWW-Authenticate': 'Basic'})

	authToken = authHeader.split(' ')[1]
	playerID = util.checkAuth(storage['players'], authToken)

	if not playerID:
		return 'Error: invalid authorization', 403

	return json.dumps({
		'id': playerID,
		'valid': True
	}, indent=4), 200


@app.route('/players', methods=['POST'])
def post_player():

	authHeader = request.headers.get('Authorization')

	if not authHeader:
		return Response('Error: unauthorized', 401, {'WWW-Authenticate': 'Basic'})

	authToken = authHeader.split(' ')[1]
	teamID = util.checkAuth(storage['teams'], authToken)

	if not teamID:
		return 'Error: invalid authorization', 403


	player = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

	player['team'] = teamID

	id = util.id()
	token = util.token()
	# TODO: Hash + Salt?
	player['token'] = token

	storage['players'][id] = player

	# DEBUG
	util.showDict(storage)

	return json.dumps({
		'id': id,
		'token': token
	}, indent=4), 201


@app.route('/players', methods=['GET'])
def get_players():

	players = deepcopy(storage['players'])

	# Remove tokens, those are secret :P
	for id in players:
		del players[id]['token']

	start = request.args.get('start', default = 0, type = int)
	count = request.args.get('count', default = None, type = int)

	players = util.paginate(players, start, count)

	return json.dumps(players, indent=4)


@app.route('/player/<id>', methods = ['GET'])
def get_player(id):

	if not id in storage['players']:
		return 'Error: Not found', 404

	player = deepcopy(storage['players'][id])

	# Remove token, that's secret :P
	del player['token']

	return json.dumps(player, indent=4)
