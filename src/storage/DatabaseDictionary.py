from pymongo import MongoClient
from collections.abc import MutableMapping

class DatabaseDictionary(MutableMapping):
    '''
    A persistent dictionary, which only accepts str keys.
    It is based and reliant on a mongoDB
    '''
    
    def __init__(self, url='localhost', port=27017):
        self.mongo_client = MongoClient(url, port)
        self.mongo_database = self.mongo_client['pjki']
        self.mongo_collection = self.mongo_database['game-history']

    def __getitem__(self, key):
        if type(key) is not str:
            raise TypeError('Key is not string')

        return self.mongo_collection.find_one({'key': key})['value']

    def __setitem__(self, key, value):
        self.mongo_collection.delete_many({'key': key})
        self.mongo_collection.insert_one({
            'key': key,
            'value': value
        })

    def __delitem__(self, key):
        self.mongo_collection.delete_many({'key': key})

    def __iter__(self):
        return iter([entry['key'] for entry in self.mongo_collection.find()])

    def __len__(self):
        return self.mongo_collection.count_documents({})
