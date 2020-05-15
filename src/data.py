from storage.DatabaseDictionary import DatabaseDictionary, setInterval
import atexit

DATABASE_KEYS = ['teams', 'players', 'games']
persistent_storage = DatabaseDictionary()


def write_database():
	for key in DATABASE_KEYS:
		persistent_storage[key] = storage[key]

storage = {
        key: persistent_storage.get(key, {})
        for key in DATABASE_KEYS
    }

write_database()

scheduled_database_writethrough = setInterval(10, write_database)

def stop_writethrough():
    scheduled_database_writethrough.cancel()

atexit.register(stop_writethrough)