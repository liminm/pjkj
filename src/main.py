from flask import Flask

app = Flask(__name__)

# Will be replaced by storage module/class
storage = {
	'games': {},
	'teams': {}
}

import game
import team
import event

if __name__ == "__main__":
	app.run()
