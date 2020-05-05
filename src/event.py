from flask import request, Response
import json
import time
from datetime import datetime

from __main__ import app, storage
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
		return 'Error: game already ended', 400

	event = json.loads(request.data.decode('UTF-8'))
	# TODO: Verify format and data

	# Get player who did move (playerA/playerB)
	# (by getting the key corresponding to the ID value)
	event['player'] = list(game['players'].keys())[
		list(game['players'].values()).index(playerID)
	]

	# Add timestamp
	now = datetime.utcnow()
	event['timestamp'] = now.isoformat()

	# Initialize details dict if it doesn't exist yet
	event.setdefault('details', {})

	# We assume events to be generally valid, checks follow later
	valid = True
	reason = ''
	endEvent = None

	# This is kinda hacky, i wish we could adapt the API to the DB here
	if event['type'] == 'surrender':
		event['details']['type'] = 'surrender'
		event['details']['winner'] = util.otherPlayer(event['player'])
		event['type'] = 'gameEnd'
		game['state']['state'] = 'completed'
		game['state']['winner'] = event['details']['winner']


	elif event['type'] == 'move':
		if len(game['events']) > 0:
			lastTime = datetime.fromisoformat(game['events'][-1]['timestamp'])
			timeDiff = (now - lastTime)
			event['details']['time'] = int(timeDiff.total_seconds() * 1000)
		else:
			# TODO: Maybe implement a 'start' signal from which we count
			event['details']['time'] = 0
		"""
		# TODO: Check move with ruleserver
		# TODO: [Idea] If we could move the changing ot state to the ruleserver (using pass-by-reference), we would save a lot of parameters and it would actually kinda make sense work separation-wise...
		valid, postFEN, gameEnd, reason = ruleServer.moveCheck(
			event['details']['move'],
			event['details']['time'],
			game['state'],
			game['events']
		)
		event['details']['postFEN'] = postFEN
		game['state']['fen'] = postFEN
		if (gameEnd):
			endEvent = {
				'type': 'gameEnd',
				'player': event['player'],
				'timestamp': event['timestamp'],
				'details': gameEnd
			}
			game['state']['state'] = 'completed'
			game['state']['winner'] = winner
		"""

	else:
		return 'Error: unknown event type', 400

	if (valid):
		game['events'].append(event)

	if (endEvent):
		game['events'].append(endEvent)

	return json.dumps({
		'valid': valid,
		'reason': reason
	}, indent=4), 201





@app.route('/game/<id>/events', methods=['GET'])
def get_events(id):

	game = storage['games'][id]

	def stream_events():

		yield '[\n'

		# We get the current length before we print old stuff, just to be sure
		# that we don't miss anything coming in while we send this out
		prevLen = len(game['events'])

		# Serve past events
		for event in game['events']:
			yield json.dumps(event, indent=4) + ',\n'

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
				yield json.dumps(game['events'][i], indent=4) + ',\n'

			prevLen = newLen

		yield ']'

	return Response(stream_events(), mimetype='text/event-stream')
