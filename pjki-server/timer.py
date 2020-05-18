import threading, time, datetime

from .data import storage
from . import util

# Get the current unix time epoch in milliseconds
def time_ms():
	return int(time.time() * 1000)

# Set a function to be executed after a certain time
def setTimeout(ms, function, args):
	t = threading.Timer(ms / 1000, function, args)
	t.start()
	return t



# This stores watcher information based on gameIDs (naturally, there can only
# be one timer running per game). It's not stored in the database because it
# includes a threading.Timer instance, which is not JSON serializable.
watchers = {}

# Watchers are ended in one of 2 ways:
# 1) The player does not respond in time, the timer triggers and handles the
#		game End
# 2) The player responds in time, the timer gets cancelled and the time is
#		calculated

# PLAYER OVERSLEPT
def watcherHandler(gameID):

	print('Watcher triggered for game ' + gameID + '!')
	game = storage['games'][gameID]
	watcher = watchers[gameID]

	# When the timer triggers for a player, it means the other won
	winner = util.opponent(watcher['player'])

	# Mark the game as completed and declare winner
	game['state']['state'] = 'completed'
	game['state']['winner'] = winner

	# Add game end event to eventstream
	game['events'].append({
		'type': 'gameEnd',
		'player': watcher['player'],
		'timestamp': datetime.datetime.utcnow().isoformat(),
		'details': {
			'type': watcher['type'],
			'winner': winner
		}
	})

	# DEBUG
	util.showDict(storage)

# Starts a timer based on the current game situation
def startWatcher(gameID, player, timeout, timeBudget):

	# Set timer for whichever time runs out first, in ms
	duration = min(timeout, timeBudget)
	timer = setTimeout(duration, watcherHandler, [gameID])

	# Add watcher info for later reference
	watchers[gameID] = {
		'timer': timer,
		'start': time_ms(),
		'type': 'timeout' if timeout < timeBudget else 'timeBudget',
		'player': player
	}

# PLAYER RESPONDS IN TIME
def stopWatcher(gameID):

	# At the start of the game, with the first move the timer for that move is
	# 'stopped' even though it was never started. This first move is counted as
	# taking no time (0 ms).
	if not gameID in watchers:
		return 0

	# Cancel the timer
	watchers[gameID]['timer'].cancel()

	# Calculate the time from the start of the timer until now
	end = time_ms()
	start = watchers[gameID]['start']

	# Remove the watcher information
	del watchers[gameID]

	return end - start
