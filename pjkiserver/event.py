from flask import Blueprint, request, Response
import json
import time
from datetime import datetime

from .storage.storage import storage, syncDB
from . import schemas, timer, rules, util


_eventstream_update_interval = 0.05 # seconds
_eventstream_heartbeat_interval = 2 # seconds


api = Blueprint('event', __name__)


@api.route('/game/<gameID>/events', methods=['POST'])
def post_event(gameID):

	game = storage['games'].get(gameID)
	if not game:
		return 'Error: Game not found', 404

	# Only players are allowed to send events to a game. Therefore, we
	# authenticate them.
	playerID, response = util.auth(storage['players'], request)

	# If authentication fails, send error message and -code
	if not playerID:
		return Response(*response)

	# Get player who sent event (playerA/playerB)
	player = util.playerFromID(game['players'], playerID)
	# If the player is not a member of this game, the token is invalid as well
	if not player:
		return 'Error: token owner not in this game', 403


	# Events can only be sent to planned or running games, never completed ones
	if game['state']['state'] == 'completed':
		return 'Error: game already ended', 409

	# Parse and validate payload
	event, error = schemas.parseAndCheck(request.data, schemas.event)
	if error:
		return Response(*error)

	# Add player who sent the event to it
	event['player'] = player

	# Add current timestamp to all events
	now = datetime.utcnow()
	event['timestamp'] = now.isoformat()

	# Initialize details dict if it doesn't exist yet
	event.setdefault('details', {})

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

		# since not every event type needs details, this couldn't be checked
		# by the schema checker before.
		if not 'move' in event.get('details', {}):
			return 'Error: Move event needs missing details.move', 400

		# Check move with ruleserver
		valid, gameEnd, reason = rules.moveCheck(game['type'], event, game['state'])
		print('> valid:', valid)

		reason = reason if not valid else util.getNiceMessage()

		if valid:
			# If everything is ok (meaning either a valid move or a surrender),
			# we log the time the move took and adjust the time Budget. Then we
			# send out the event indicating what happened.
			duration = timer.stopWatcher(gameID)
			game['players'][player]['timeBudget'] -= duration
			event['details']['time'] = duration
			game['events'].append(event)

		else:
			# Return error if invalid
			return json.dumps({
				'valid': False,
				'reason': reason
			}, indent=4), 200

	else:
		return 'Error: unknown event type', 400

	if gameEnd:
		# If the move check indicated that this move ends the game or a player
		# surrendered, we mark the game as completed and declare the winner.
		# We also send an event that informs clients of the game end.
		game['state']['state'] = 'completed'
		game['state']['winner'] = gameEnd['winner']

		endEvent = {
			'type': 'gameEnd',
			'player': player,
			'timestamp': now.isoformat(),
			'details': gameEnd
		}

		game['events'].append(endEvent)

		# Stop any timers that are running for this game
		timer.stopWatcher(gameID)

	else:
		# If the game continues, we start the timer for the next move.
		# The state is set to 'running' here because a game starts as soon as
		# the first valid move is made.
		game['state']['state'] = 'running'
		opponent = util.opponent(player)
		timer.startWatcher(gameID, opponent, game['players'][opponent])

	# Save changes to persistent DB
	syncDB(['games'])

	return json.dumps({
		'valid': True,
		'reason': util.getNiceMessage()
	}, indent=4), 201





@api.route('/game/<gameID>/events', methods=['GET'])
def get_events(gameID):

	game = storage['games'].get(gameID)
	if not game:
		return 'Error: Game not found', 404

	# A GET on the events results in a continuous eventstream in the SSE format
	# (See https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
	# This means a JS client can easily retrieve each chunk of data as an event
	# almost instantly after is arrives on the server.
	# That means this function and its while-loop stay running in their handler
	# thread as long as a) the client is connected or b) the game is running,
	# while continuously feeding back data with the `yield` keyword.
	def stream_events():

		print('Oppening eventstream on game ' + gameID)

		# Some SSE clients seem to not start receiving until the first
		# line/byte is sent. This does just that for them and hopefully won't
		# break anything else.
		yield '\n\n'

		# We get the current length before we print old stuff, just to be sure
		# that we don't miss anything coming in while we send this out
		prevLen = len(game['events'])

		# Serve past events
		for event in game['events']:
			yield 'data: ' + json.dumps(event) + '\n\n'

		tickCounter = 0

		try:
			# Just in case new events arrived while the state was 'completed',
			# we give the option to print those regardless of the state
			while game['state']['state'] != 'completed' or len(game['events']) > prevLen:

				# Wait for new events to appear
				time.sleep(_eventstream_update_interval)
				tickCounter += 1

				# Check event array for new entries
				newLen = len(game['events'])
				newEventCount = newLen - prevLen

				# Tricky trick here: we want the last couple events in the
				# correct order, by using range from negative to 0, we get
				# exactly that:
				# range(-3, 0) -> [-3, -2, -1]
				for i in range(-newEventCount, 0):
					yield 'data: ' + json.dumps(game['events'][i]) + '\n\n'

				prevLen = newLen

				# Send a heartbeat every couple of seconds
				# This is done because whenever a client disconnects/closes the
				# eventstream connection and no events are generated, this
				# handler stays running because a closed connection can't be
				# detected without sending data to it and getting an error.
				# That's a problem because every handler takes up a thread on
				# the prod (uwsgi) server, which are limited in number, leading
				# the entire server to lock up when all threads are used up
				# handling a closed connection.
				# Therefore we forcefully send data regularly to end this
				# handler when there is no recipient anymore.
				heartbeatIntervalTicks = int(_eventstream_heartbeat_interval /
												_eventstream_update_interval)
				if (tickCounter % heartbeatIntervalTicks == 0):
					yield ': heartbeat\n\n'
					tickCounter = 0

			print('Eventstream ended on game ' + gameID)

		except GeneratorExit:
			print('Client closed eventstream on game ' + gameID)

		return

	# Start the eventstream. The mimetype is necessary for the JS EventSource
	# API.
	return Response(stream_events(), 200, mimetype='text/event-stream')
