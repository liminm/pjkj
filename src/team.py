from flask import request
import json
from copy import deepcopy

from __main__ import app, storage
import util


@app.route('/teams', methods=['POST'])
def post_team():

	team = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

	id = util.id()
	token = util.token()
	# TODO: Hash + Salt?
	team['token'] = token

	storage['teams'][id] = team

	# DEBUG
	util.showDict(storage)

	return json.dumps({
		'id': id,
		'token': token
	}), 201


@app.route('/teams', methods=['GET'])
def get_teams():

	teams = deepcopy(storage['teams'])

	# Remove tokens, those are secret :P
	for id in teams:
		del teams[id]['token']

	return json.dumps(teams)


@app.route('/team/<id>', methods = ['GET'])
def get_team(id):

	if not id in storage['teams']:
		return 'Error: Not found', 404

	team = deepcopy(storage['teams'][id])

	# Remove token, that's secret :P
	del team['token']

	return json.dumps(team)
