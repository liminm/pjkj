from flask import request
import json

from __main__ import app, storage
import util

@app.route('/games', methods=['POST'])
def post_game():
	data = json.loads(request.data.decode('UTF-8'))
	id = util.randomID()
	storage['games'][id] = data

	# DEBUG
	util.showDict(storage)

	return json.dumps({
		'id': id
	}), 201

@app.route('/games', methods=['GET'])
def get_games():
	# TODO: This won't return _all_ game data, just what's necessary to display a list
	# TODO: AS ARRAY
	return json.dumps(storage['games'])

@app.route('/game/<id>', methods = ['GET'])
def get_game(id):
	if id in storage['games']:
		return json.dumps(storage['games'][id])
	else:
		return 'Error: Not found', 404
