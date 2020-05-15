from flask import request, Response
import json
import time
from datetime import datetime

from __main__ import app, storage
import timer
import util


@app.route('/game/<id>/events', methods=['POST'])
def post_event(id):

	game = storage['games'][id]

	# Only players are allowed to send events to a game. Therefore, we
	# authenticate them.
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

	# Search this token in the database to find the corresponding player
	playerID = util.checkAuth(storage['players'], authToken)

	# Verify that the authenticated player is a member of this game
	isInGame = playerID in game['players'].values()

	# If no player has this token or the player is not a member of this game,
	# the token is invalid
	if not playerID or not isInGame:
		return 'Error: invalid authorization', 403


	# Events can only be sent to planned or running games, never completed ones
	if game['state']['state'] == 'completed':
		return 'Error: game already ended', 409

	# Get the payload and parse it
	event = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

	# Get player who did move (playerA/playerB)
	player = util.playerFromID(game['players'], playerID)
	event['player'] = player

	# Add current timestamp to all events
	now = datetime.utcnow()
	event['timestamp'] = now.isoformat()

	# Initialize details dict if it doesn't exist yet
	event.setdefault('details', {})

	# We assume this is a valid event, checks follow later
	valid = True
	gameEnd = None
	reason = ''

	# The 'surrender' is the only non-move event clients can submit. It results
	# in a 'gameEnd' event with type 'surrender', while the opponent wins.
	if event['type'] == 'surrender':
		gameEnd = {
			'type': 'surrender',
			'winner': util.opponent(player)
		}

	# The most common event clients submit is the move, which is processed by
	# the ruleserver.
	elif event['type'] == 'move':
		# TODO: Check move with ruleserver
		#valid, gameEnd, reason = ruleServer.moveCheck(event, game['state'])
		print('NYI')

	else:
		return 'Error: unknown event type', 400

	# If the move check indicated that this move ends the game or a player
	# surrendered, we mark the game as completed and declare the winner.
	# We also prepare the event that informs clients of the game end.
	if gameEnd:
		game['state']['state'] = 'completed'
		game['state']['winner'] = gameEnd['winner']
		event['type'] = 'gameEnd'
		event['details'] = gameEnd

	# If everything is valid (meaning either a valid move or a game end), we
	# log the time the move took and adjust the time Budget. Then we send out
	# the event indicating what happened.
	if valid:
		duration = timer.stopWatcher(id)
		event['details']['time'] = duration
		game['state']['timeBudgets'][player] -= duration
		game['events'].append(event)

		# If the game continues, we start the timer for the next move.
		# The state is set to 'running' here because a game starts as soon as
		# the first valid move is made.
		if not gameEnd:
			game['state']['state'] = 'running'
			opponent = util.opponent(player)
			timer.startWatcher(id, opponent,
				game['settings']['timeout'],
				game['state']['timeBudgets'][opponent])

	# DEBUG
	util.showDict(storage)

	return json.dumps({
		'valid': valid,
		'reason': reason
	}, indent=4), 201





@app.route('/game/<id>/events', methods=['GET'])
def get_events(id):

	game = storage['games'][id]

	# A GET on the events results in a continuous eventstream in the SSE format
	# (See https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
	# This means a JS client can easily retrieve each chunk of data as an event
	# almost instantly after is arrives on the server.
	# That means this function and its while-loop stay running in their handler
	# thread as long as a) the client is connected or b) the game is running,
	# while continuously feeding back data with the `yield` keyword.
	def stream_events():

		# We get the current length before we print old stuff, just to be sure
		# that we don't miss anything coming in while we send this out
		prevLen = len(game['events'])

		# Serve past events
		for event in game['events']:
			yield 'data: ' + json.dumps(event) + '\n\n'

		# Just in case new events arrived while the state was set to completed,
		# we give the option to print those regardless of the state
		while game['state']['state'] != 'completed' or len(game['events']) > prevLen:

			# Wait for new events to appear
			time.sleep(.2)

			# Check event array for new entries
			newLen = len(game['events'])
			newEventCount = newLen - prevLen

			# Tricky trick here: we want the last couple events in the correct
			# order, by using range from negative to 0, we get exactly that:
			# range(-3, 0) -> [-3, -2, -1]
			for i in range(-newEventCount, 0):
				yield 'data: ' + json.dumps(game['events'][i]) + '\n\n'

			prevLen = newLen

	# Start the eventstream. The mimetype is necessary for the JS EventSource
	# API.
	return Response(stream_events(), mimetype='text/event-stream')
