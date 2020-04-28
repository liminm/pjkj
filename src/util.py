import string
import random

id_len = 42

def randomString(n):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def randomID():
	return randomString(id_len)
