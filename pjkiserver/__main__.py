import signal
from flask import Flask

app = Flask(__name__)

# Permanent storage / database handling
from .storage import storage
from . import timer

# These modules contain the endpoints and their handlers
from . import team
from . import player
from . import game
from . import event

app.register_blueprint(team.api)
app.register_blueprint(player.api)
app.register_blueprint(game.api)
app.register_blueprint(event.api)

@app.route('/')
def get_root():
	return "Error: No Endpoint selected. See docs/API.md for reference.", 404

def shutdown(*args):
	# Stop all subsystems
	print("Stopping server...")
	timer.stopAll()
	print("Bye!")
	exit(0)

# Graceful shutdowns
# TODO: Make Cross-Platform
signal.signal(signal.SIGINT,  shutdown)
signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGQUIT, shutdown)

# Start the flask server if run from terminal
if __name__ == "__main__":

	# Tell storage to print out entire database on changes
	storage.verbosePrinting = True

	# Just allow everything to avoid the hassle when running locally.
	@app.after_request
	def add_headers(response):
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = '*'
		response.headers['Access-Control-Allow-Headers'] = '*'
		return response

	app.run()
