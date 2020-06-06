import json
from pymongo.errors import ConnectionFailure

from .database import DatabaseDictionary

# The 3 base collections
DATABASE_KEYS = ['teams', 'players', 'games']

# Local, volatile storage for quick access
storage = {
	key: {} for key in DATABASE_KEYS
}


# To be set by importer if they wish to print entire DB on save
verbosePrinting = False

# Debug function to show the current database contents
def printStorage():
	if verbosePrinting:
		# Clear terminal screen
		print('\033c')
		print(json.dumps(storage, indent=4))
	else:
		print("Storage now has {} teams, {} players and {} games.".format(
			len(storage['teams']),
			len(storage['players']),
			len(storage['games'])
		))


# Handle for the persistent database object
persistentDB = None

# Sync local dict into persistent database
def syncDB(keys=DATABASE_KEYS):

	printStorage()

	if not persistentDB:
		return

	for key in keys:
		persistentDB[key] = storage[key]


# try to connect to mongoDB and register the writethroughs and handle the signals
# if not connectable just start the development enviroement where storage is not synced with the mongoDB and therefore NOT SAVED
try:
	# Persistent storage
	persistentDB = DatabaseDictionary()

	# Initialize with persistent storage values
	for key in DATABASE_KEYS:
		storage[key] = persistentDB.get(key) or {}

	# Save initial state in case persistent DB was uninitialized
	syncDB()

except ConnectionFailure:
	# Inform users that data will not be saved
	print("DATABASE COULD NOT BE REACHED")
	print("`storage` will not be saved persistently")
	print("THIS MODE IS FOR DEVELOPMENT PURPOSES ONLY")
