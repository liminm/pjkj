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

	authHeader = request.headers.get('Authorization')

	if not authHeader:
		return Response('Error: unauthorized', 401, {'WWW-Authenticate': 'Basic'})

	authToken = authHeader.split(' ')[1]
	playerID = util.checkAuth(storage['players'], authToken)
	isInGame = playerID in game['players'].values()

	if not playerID or not isInGame:
		return 'Error: invalid authorization', 403


	if game['state']['state'] == 'completed':
		return 'Error: game already ended', 409

	event = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

	# Get player who did move (playerA/playerB)
	# (by getting the key corresponding to the ID value)
	player = util.playerFromID(game['players'], playerID)
	event['player'] = player

	# Add timestamp
	now = datetime.utcnow()
	event['timestamp'] = now.isoformat()

	# Initialize details dict if it doesn't exist yet
	event.setdefault('details', {})

	# We assume this is a valid event, checks follow later
	valid = True
	gameEnd = None
	reason = ''

	if event['type'] == 'surrender':
		gameEnd = {
			'type': 'surrender',
			'winner': util.opponent(player)
		}

	elif event['type'] == 'move':
		# TODO: Check move with ruleserver
		#valid, gameEnd, reason = ruleServer.moveCheck(event, game['state'])
		print('NYI')

	else:
		return 'Error: unknown event type', 400

	if gameEnd:
		game['state']['state'] = 'completed'
		game['state']['winner'] = gameEnd['winner']
		event['type'] = 'gameEnd'
		event['details'] = gameEnd

	if valid:
		duration = timer.stopWatcher(id)
		event['details']['time'] = duration
		game['state']['timeBudgets'][player] -= duration
		game['events'].append(event)

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

	return Response(stream_events(), mimetype='text/event-stream')
