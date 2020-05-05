from flask import request, Response

import json
import time

from __main__ import app, storage
import util

events = []

def stream_events(id):
	yield '[\n'
	# TODO: Serve past events
	pl = len(events)
	while True:
		time.sleep(.1)
		# Wait until new event appears
		# (Check event array for new entries)

		if len(events) > pl:
			yield json.dumps(events[-1]) + ',\n'

		pl = len(events)
	yield ']'

@app.route('/game/<id>/events', methods=['GET'])
def get_events(id):
	return Response(stream_events(id), mimetype='text/event-stream')

@app.route('/game/<id>/events', methods=['POST'])
def post_event(id):
	# TODO: Process event
	events.append(json.loads(request.data))
	return json.dumps({
		'valid': False,
		'reason': ''
	})
