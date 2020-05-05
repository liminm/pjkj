import string
import random
import json

id_len = 16
token_len = 42

def randomString(n):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def id():
	return randomString(id_len)

def token():
	return randomString(token_len)

def showDict(dict):
	print('\033c')
	print(json.dumps(dict, indent=4))
