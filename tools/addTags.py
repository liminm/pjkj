import sys
import fileinput

from pjkiserver.storage.storage import storage, syncDB

try:
	tag = sys.argv[2]
except:
	print(f'Need 2 arguments (`{sys.argv[0]} < filename | - > < tag >`)')
	exit()




games = storage['games']
counter = 0

for line in fileinput.input(sys.argv[1:2]):

	id = line.strip()

	if not id in games:
		continue

	games[id]['tags'] = games[id].get('tags') or []
	games[id]['tags'].append(tag)
	counter += 1




print(counter, 'games will be changed.')

val = ''
while not (val in ['yes', 'no']):
	val = input('Are you sure you want to proceed? (yes/no) ')

if (val != 'yes'):
	exit()

print('Writing...')
syncDB(['games'])
