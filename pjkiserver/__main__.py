import signal
from flask import Flask

app = Flask(__name__)

@app.after_request
def add_headers(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = '*'
	response.headers['Access-Control-Allow-Headers'] = '*'
	return response

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

def shutdown(*args):
	print("Stopping server...")
	timer.stopAll()
	storage.stop()
	print("Bye!")
	exit(0)

# Graceful shutdowns
signal.signal(signal.SIGINT,  shutdown)
signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGQUIT, shutdown)

# Start the flask server
if __name__ == "__main__":
	app.run()
