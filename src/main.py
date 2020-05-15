from flask import Flask

app = Flask(__name__)

# Will be replaced by storage module/class
storage = {
	'teams': {},
	'players': {},
	'games': {}
}

# These modules contain the endpoints and their handlers
import team
import player
import game
import event

# Start the flask server
if __name__ == "__main__":
	app.run()
