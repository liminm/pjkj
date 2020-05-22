import signal

from .database import DatabaseDictionary
from .scheduler import SetInterval

from pymongo.errors import ConnectionFailure

# The 3 base collections
DATABASE_KEYS = ['teams', 'players', 'games']

# try to connect to mongoDB and register the writethroughs and handle the signals
# if not connectable just start the development enviroement where storage is not synced with the mongoDB and therefore NOT SAVED
try:
	# Persistent storage
	persistent_storage = DatabaseDictionary()

	# Local, volatile storage for quick access
	# Initialize with persistent storage values
	storage = {
		key: (persistent_storage.get(key) or {}) for key in DATABASE_KEYS
	}

	# Sync local dict into persistent database
	def write_database():
		for key in DATABASE_KEYS:
			persistent_storage[key] = storage[key]

	# Save initial state
	write_database()

	# Start a timer to save state every 10 seconds
	scheduled_database_writethrough = SetInterval(10, write_database)

	# When stopping the server, save the state to the database and stop the timer
	def stop_writethrough(*args):
		print("Stopping server...")
		scheduled_database_writethrough.cancel()
		write_database()
		print("Finished dumping DB. Bye!")
		exit(0)

	# Make the server save state if a termination signal is received
	signal.signal(signal.SIGTERM, stop_writethrough)
	signal.signal(signal.SIGINT, stop_writethrough)

except ConnectionFailure:
	# Provide an empty, non-synced, volatile storage dict
	storage = {
		key: {} for key in DATABASE_KEYS
	}

	# Inform users that data will not be saved
	print("DATABASE COULD NOT BE REACHED")
	print("`storage` will not be saved persistently")
	print("THIS MODE IS FOR DEVELOPMENT PURPOSES ONLY")
