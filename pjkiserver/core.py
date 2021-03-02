import atexit
from flask import Flask

app = Flask(__name__)

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

# Graceful shutdowns
atexit.register(shutdown)
