import sys
import fileinput

from pjkiserver.storage.storage import storage, syncDB

try:
	tag = sys.argv[1]
except:
	print(f'Need 1 argument (`{sys.argv[0]} < tag >`)')
	exit()




games = storage['games']
counter = 0

for id in games:

	if tag in games[id].get('tags', []):
		games[id]['tags'].remove(tag)
		counter += 1




print(counter, 'games will be changed.')

val = ''
while not (val in ['yes', 'no']):
	val = input('Are you sure you want to proceed? (yes/no) ')

if (val != 'yes'):
	exit()

print('Writing...')
syncDB(['games'])
