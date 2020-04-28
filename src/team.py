from flask import request
import json

from __main__ import app, storage
import util

@app.route('/teams', methods=['POST'])
def post_team():
	# TODO: Specify team object standard
	data = json.loads(request.data.decode('UTF-8'))
	id = util.randomID()
	storage['teams'][id] = data

	# DEBUG
	print(json.dumps(storage))

	return json.dumps({
		'id': id
	}), 201

@app.route('/teams', methods=['GET'])
def get_teams():
	# TODO: Specify team object standard
	return json.dumps(storage['teams'])

@app.route('/team/<id>', methods = ['GET'])
def get_team(id):
	if id in storage['teams']:
		return json.dumps(storage['teams'][id])
	else:
		return 'Error: Not found', 404
