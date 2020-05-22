import string
import random
import json

id_len = 16
token_len = 42

# Generate a random string of letters (uppercase + lowercase + digits)
# Not cryptographically random, but good enough
def randomString(n):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

# Function to generate IDs
def id():
	return randomString(id_len)

# Function to generate Tokens
def token():
	return randomString(token_len)

# Debug function to show the current database contents
def showDict(dict):
	# Clear terminal screen
	print('\033c')
	print(json.dumps(dict, indent=4))

# Check authorization token by searching through all candidates, returning the
# id of the candidate that matches the token
def checkAuth(dict, token):
	for id in dict:
		if dict[id]['token'] == token:
			return id
	return None

def auth(dict, request):

	# Authentication tokens are sent with the Authorization header as follows:
	# Authorization: Basic abcdefgXYZ123...
	# Where the last part is the token.
	authHeader = request.headers.get('Authorization')

	# If the header is not present, we inform the client that this endpoint
	# requires authentication
	if not authHeader:
		return None, ('Error: Unauthorized (Authorization missing)', 401,
			{'WWW-Authenticate': 'Basic'})

	# Separate into 'Basic' and '<Token>'
	try:
		authType, authToken = authHeader.strip().split(' ')
	except ValueError:
		return None, ('Error: Malformed auth header: Must be 2 words', 400)

	# Ensure the normal auth type is given
	if authType != 'Basic':
		return None, ('Error: Only "Basic" auth supported', 400)

	# Search this token in the database to find the corresponding player
	id = checkAuth(dict, authToken)

	# If no entity has this token, it's invalid
	if not id:
		return None, ('Error: Invalid authorization (no such token)', 403)

	return id, None

# Utility function to find the opposite player
def opponent(player):
	if player == 'playerA':
		return 'playerB'
	elif player == 'playerB':
		return 'playerA'
	return None

# For a game, find out which playerID results in which side
# AKA in the `players` dict, find the key corresponding to a value
# Done by taking the index of the correct value and using it to get the key
def playerFromID(players, id):
	return list(players.keys())[ list(players.values()).index(id) ]

# Get a subslice of a dict. This would be way easier if it was an array and
# also relies on the fact that dicts are ordered by insertion time. Yikes.
def paginate(listDict, start, count):

	# Turn dict into list of (key, val) tuples
	dictList = list(listDict.items())

	# the 'last' element in python slice syntax is exactly start+count, 0-based
	# if no count is given, use None to get all remaining items
	end = start + count if count else None

	# Slice the list
	truncList = dictList[start:end]

	# Turn it back into a dict
	return dict(truncList)

# Filter games by state
def filterState(listDict, state):

	# Filtering by * is no filtering at all!
	if (state == '*'):
		return listDict

	# Turn dict into list of (key, val) tuples
	dictList = list(listDict.items())

	# Use a lambda function to compare each values state with the filter state
	# And keep only matching (key, value) pairs
	filteredList = list(
		filter(lambda el: el[1]['state']['state'] == state, dictList))

	# Turn it back into a dict
	return dict(filteredList)
