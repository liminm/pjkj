from .database import DatabaseDictionary
from .scheduler import SetInterval

from pymongo.errors import ConnectionFailure

# The 3 base collections
DATABASE_KEYS = ['teams', 'players', 'games']

# try to connect to mongoDB and register the writethroughs and handle the signals
# if not connectable just start the development enviroement where storage is not synced with the mongoDB and therefore NOT SAVED
try:
	# Persistent storage
	persistentDB = DatabaseDictionary()

	# Local, volatile storage for quick access
	# Initialize with persistent storage values
	storage = {
		key: (persistentDB.get(key) or {}) for key in DATABASE_KEYS
	}

	# Sync local dict into persistent database
	def dumpDatabase():
		for key in DATABASE_KEYS:
			persistentDB[key] = storage[key]

	# Save initial state
	dumpDatabase()

	# Start a timer to save state every 10 seconds
	dumpInterval = SetInterval(10, dumpDatabase)

	# When shutting down, save the state to the database and stop the timer
	def stop():
		print("Dumping DB...")
		dumpInterval.cancel()
		dumpDatabase()
		print("Finished dumping DB")

except ConnectionFailure:
	# Provide an empty, non-synced, volatile storage dict
	storage = {
		key: {} for key in DATABASE_KEYS
	}

	def stop():
		print("No DB to dump")

	# Inform users that data will not be saved
	print("DATABASE COULD NOT BE REACHED")
	print("`storage` will not be saved persistently")
	print("THIS MODE IS FOR DEVELOPMENT PURPOSES ONLY")
