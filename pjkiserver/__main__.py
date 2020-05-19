from flask import Flask

app = Flask(__name__)

# Permanent storage / database handling
from .storage.storage import storage

# TESTING:
storage['teams'] = {}
storage['players'] = {}
storage['games'] = {}

# These modules contain the endpoints and their handlers
from . import team
from . import player
from . import game
from . import event

app.register_blueprint(team.api)
app.register_blueprint(player.api)
app.register_blueprint(game.api)
app.register_blueprint(event.api)

# Start the flask server
if __name__ == "__main__":
	app.run()
