import sys

from pjkiserver.storage.storage import storage, syncDB

try:
	mode = sys.argv[1]
except:
	print(f'Need at least 1 argument (`{sys.argv[0]} <gameID1>, <gameID2>`)')
	exit()

games = storage['games']
delete = sys.argv[1:]

print(f'Games to delete ({len(delete)}):')
print(delete)

for id in delete:
	del games[id]


val = ''
while not (val in ['yes', 'no']):
	val = input('Are you sure you want to proceed? (yes/no) ')

if (val != 'yes'):
	exit()

print('Writing...')
syncDB()
