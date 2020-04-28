from flask import Response

import json
import time

from __main__ import app, storage
import util

def stream_events():
	yield '[\n'
	while True:
		time.sleep(1)
		yield '{ move: test-' + util.randomString(8) + ' },\n'
	yield ']'

@app.route('/game/<id>/events', methods=['GET'])
def get_events(id):
	# TODO: Serve past & new events
	return Response(stream_events(), mimetype='text/event-stream')

@app.route('/game/<id>/events', methods=['POST'])
def post_event(id):
	# TODO: Process event
	return json.dumps({
		'valid': False,
		'reason': ''
	})
