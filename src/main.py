from flask import Flask

app = Flask(__name__)


# These modules contain the endpoints and their handlers
import data
import team
import player
import game
import event

# Start the flask server
if __name__ == "__main__":
	app.run()
	