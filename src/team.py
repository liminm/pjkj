from flask import Blueprint, request
import json
from copy import deepcopy

from data import storage
import util


api = Blueprint('team', __name__)


# This endpoint is only for the frontend to verify tokens before saving them
@api.route('/teamlogin', methods = ['GET'])
def get_teamlogin():

	# Verify Authorization
	teamID, response = util.auth(storage['teams'], request)

	# If authentication fails, send error message and -code
	if not teamID:
		return Response(*response)

	return json.dumps({
		'id': teamID,
		'valid': True
	}, indent=4), 200


@api.route('/teams', methods=['POST'])
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


@api.route('/teams', methods=['GET'])
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


@api.route('/team/<id>', methods = ['GET'])
def get_team(id):

	if not id in storage['teams']:
		return 'Error: Not found', 404

	# In order to not accidentally remove the tokens from the database, we copy
	# the entire dict here.
	team = deepcopy(storage['teams'][id])

	# Remove token, since it's a secret :P
	del team['token']

	return json.dumps(team, indent=4)
