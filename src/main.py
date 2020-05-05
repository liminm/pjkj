from flask import Flask

app = Flask(__name__)

# Will be replaced by storage module/class
storage = {
	'teams': {},
	'players': {},
	'games': {}
}

import team
import player
import game
import event

if __name__ == "__main__":
	app.run()
