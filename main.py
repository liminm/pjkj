from flask import Flask, request, Response
app = Flask(__name__)

import time
import random
import string

active_games = dict()

# das sollte später durch eine MongoDB ersetzt werden
# kann dann einfach als docker container gestartet werden
# => einfache integration
game_history = dict()
user_data = dict()

@app.route('/login', methods=['POST'])
def hello_world():
    return 'Hello, World!'

@app.route('/register', methods=['POST'])
def register():
    print(request.form)

    if not request.form.get('username'):
        return('Username for registration missing', 400)

    if not request.form.get('password'):
        return('Password for registration missing', 400)

    if user_data.get('username'):
        return('Username already taken', 400)

    user_data[request.form['username']] = request.form['password']
    return ('User is registered', 200)

# @app.route('/start_game', methods=['POST'])
# def start_game():

def generateRandomString(n):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def stream_events():
    while True:
        time.sleep(1)
        yield 'event: move\ndata: test-' + generateRandomString(8) + '\n\n'

@app.route('/eventstream', methods=['GET'])
def eventstream():
    r = Response(stream_events(), mimetype='text/event-stream')
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r



if __name__ == "__main__":
    app.run()
