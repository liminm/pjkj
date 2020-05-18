from flask import Flask

app = Flask(__name__)

# Permanent storage / database handling
import data

# TESTING:
data.storage['teams'] = {}
data.storage['players'] = {}
data.storage['games'] = {}

# These modules contain the endpoints and their handlers
import team
import player
import game
import event

# Start the flask server
if __name__ == "__main__":
	app.run()
