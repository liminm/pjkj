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
# AKA in the `players` dict, find the key corresponding to a value with that id
def playerFromID(players, id):
	# Done by taking the first result of a list comprehension that assembles a
	# list of keys matching that value's id.
	# Granted, it would probably be faster to do a quick if else for this, but
	# would that be this fancy? No? I thought so. :P
	playerList = [k for k, v in players.items() if v['id'] == id]
	return playerList[0] if len(playerList) else None

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

	# Use a lambda function to compare each value's state with the filter state
	# And keep only matching (key, value) pairs
	filteredList = list(
		filter(lambda el: el[1]['state']['state'] == state, dictList))

	# Turn it back into a dict
	return dict(filteredList)

# Filter games by tag
def filterTag(listDict, tag):

	# Filtering by * is no filtering at all!
	if (tag == '*'):
		return listDict

	# Turn dict into list of (key, val) tuples
	dictList = list(listDict.items())

	# Use a lambda function to see if each value's tag list contains the tag
	# And keep only matching (key, value) pairs
	filteredList = list(
		filter(lambda el: tag in el[1]['tags'], dictList))

	# Turn it back into a dict
	return dict(filteredList)

def filterTeam(listDict, teamID):

	# Filtering by * is no filtering at all!
	if (teamID == '*'):
		return listDict

	# Turn dict into list of (key, val) tuples
	dictList = list(listDict.items())

	# Use a lambda function to compare each value's team with the filter team
	# And keep only matching (key, value) pairs
	filteredList = list(
		filter(lambda el: el[1]['team'] == teamID, dictList))

	# Turn it back into a dict
	return dict(filteredList)

def getNiceMessage():
	messages = [
		'Well done!',
		'Good boy',
		'Love you!',
		'<3',
		':)',
		'¯\_(ツ)_/¯',
		'BTW, you\'re beautiful',
		'Thank you!',
		';)',
		'xoxo',
		'*fanfare*',
		'https://youtu.be/dQw4w9WgXcQ',
		'😍',
		'Smart move!',
		'Solid choice',
		'Checks out'
	]
	return random.choice(messages)
