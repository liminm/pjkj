import threading, time, datetime

from __main__ import storage
import util

def time_ms():
	return int(time.time() * 1000)

def setTimeout(ms, function, args):
	t = threading.Timer(ms / 1000, function, args)
	t.start()
	return t



watchers = {}

# PLAYER OVERSLEPT
def watcherHandler(gameID):
	print('Watcher triggered for game ' + gameID + '!')
	game = storage['games'][gameID]
	watcher = watchers[gameID]

	winner = util.opponent(watcher['player'])

	game['state']['state'] = 'completed'
	game['state']['winner'] = winner

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

def startWatcher(gameID, player, timeout, timeBudget):
	# Whichever runs out first, ms
	duration = min(timeout, timeBudget)
	timer = setTimeout(duration, watcherHandler, [gameID])
	watchers[gameID] = {
		'timer': timer,
		'start': time_ms(),
		'type': 'timeout' if timeout < timeBudget else 'timeBudget',
		'player': player
	}

# PLAYER RESPONDS IN TIME
def stopWatcher(gameID):
	if not gameID in watchers:
		return 0
	watchers[gameID]['timer'].cancel()
	end = time_ms()
	start = watchers[gameID]['start']
	del watchers[gameID]
	return end - start


"""
CASE 1:
-> Via flask handler

** Find corresponding timer **
->

- Cancel timer
- Update timeBudget

"""
