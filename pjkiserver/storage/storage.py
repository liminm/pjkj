from .database import DatabaseDictionary
from .scheduler import SetInterval

from pymongo.errors import ConnectionFailure

# The 3 base collections
DATABASE_KEYS = ['teams', 'players', 'games']

persistentDB = None

# Local, volatile storage for quick access
storage = {
	key: {} for key in DATABASE_KEYS
}

dumpInterval = None


# Sync local dict into persistent database
def dumpDatabase():
	print("Writing storage to DB with {} teams, {} players and {} games.".format(len(storage['teams']), len(storage['players']), len(storage['games'])))
	for key in DATABASE_KEYS:
		persistentDB[key] = storage[key]


# When shutting down, save the state to the database and stop the timer
def stop():

	if (dumpInterval):
		print("Stopping DB dump timer")
		dumpInterval.cancel()

	if (persistentDB):
		print("Dumping DB...")
		dumpDatabase()
		print("Finished dumping DB")
	else:
		print("No DB connected, nothing to dump.")


# try to connect to mongoDB and register the writethroughs and handle the signals
# if not connectable just start the development enviroement where storage is not synced with the mongoDB and therefore NOT SAVED
try:
	# Persistent storage
	persistentDB = DatabaseDictionary()

	# Initialize with persistent storage values
	for key in DATABASE_KEYS:
		storage[key] = persistentDB.get(key) or {}

	print("Initialized storage from DB with {} teams, {} players and {} games.".format(len(storage['teams']), len(storage['players']), len(storage['games'])))

	# Save initial state
	dumpDatabase()

	# Start a timer to save state every 10 seconds
	dumpInterval = SetInterval(10, dumpDatabase)

except ConnectionFailure:
	# Inform users that data will not be saved
	print("DATABASE COULD NOT BE REACHED")
	print("`storage` will not be saved persistently")
	print("THIS MODE IS FOR DEVELOPMENT PURPOSES ONLY")
