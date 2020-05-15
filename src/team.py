from flask import request
import json
from copy import deepcopy

from __main__ import app, storage
import util


# This endpoint is only for the frontend to verify tokens before saving them
@app.route('/teamlogin', methods = ['GET'])
def get_teamlogin():

	# Authentication tokens are sent with the Authorization header as follows:
	# Authorization: Basic abcdefgXYZ123...
	# Where the last part is the token.
	authHeader = request.headers.get('Authorization')

	# If the header is not present, we inform the client that this endpoint
	# requires authentication
	if not authHeader:
		return Response('Error: unauthorized', 401, {'WWW-Authenticate': 'Basic'})

	# Remove the 'Basic '-part to get the token
	authToken = authHeader.split(' ')[1]

	# Search this token in the database to find the corresponding team
	teamID = util.checkAuth(storage['teams'], authToken)

	# If no team has this token, it's invalid
	if not teamID:
		return 'Error: invalid authorization', 403

	return json.dumps({
		'id': teamID,
		'valid': True
	}, indent=4), 200


@app.route('/teams', methods=['POST'])
def post_team():

	# Get the payload and parse it
	team = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

	# Generate new id and token for this new team
	id = util.id()
	token = util.token()
	# TODO: Hash + Salt?
	team['token'] = token

	# Add the team to the database
	storage['teams'][id] = team

	# DEBUG
	util.showDict(storage)

	return json.dumps({
		'id': id,
		'token': token
	}, indent=4), 201


@app.route('/teams', methods=['GET'])
def get_teams():

	# In order to not accidentally remove the tokens from the database, we copy
	# the entire dict here.
	teams = deepcopy(storage['teams'])

	# Remove tokens, since they're secrets :P
	for id in teams:
		del teams[id]['token']

	# Clients might only want a slice of the collection, which they can specify
	# using these URL parameters
	start = request.args.get('start', default = 0, type = int)
	count = request.args.get('count', default = None, type = int)

	teams = util.paginate(teams, start, count)

	return json.dumps(teams, indent=4)


@app.route('/team/<id>', methods = ['GET'])
def get_team(id):

	if not id in storage['teams']:
		return 'Error: Not found', 404

	# In order to not accidentally remove the tokens from the database, we copy
	# the entire dict here.
	team = deepcopy(storage['teams'][id])

	# Remove token, since it's a secret :P
	del team['token']

	return json.dumps(team, indent=4)
