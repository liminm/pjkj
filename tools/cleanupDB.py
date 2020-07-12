import sys

from pjkiserver.storage.storage import storage, syncDB

try:
	mode = sys.argv[1]
except:
	print(f'Need 1 argument (`{sys.argv[0]} < unstarted | unfinished >`)')
	exit()

print("Before: {} teams, {} players and {} games.".format(
	len(storage['teams']),
	len(storage['players']),
	len(storage['games'])
))



games = storage['games']
delete = []

if mode == 'unstarted':
	for id in games:
		if games[id]['state']['state'] == 'planned':
			delete.append(id)

elif mode == 'unfinished':
	for id in games:
		if games[id]['state']['state'] != 'completed':
			delete.append(id)

else:
	print('Unknown operation')
	exit()

print(f'Games to delete ({len(delete)}):')
print(delete)

for id in delete:
	del games[id]




gamePlayers = set()
for id in games:
	gamePlayers.add(games[id]['players']['playerA']['id'])
	gamePlayers.add(games[id]['players']['playerB']['id'])

players = storage['players']
delete = []

for id in players:
	if not id in gamePlayers:
		delete.append(id)

print(f'Games to delete ({len(delete)}):')
print(delete)

for id in delete:
	del players[id]




playerTeams = set()
for id in players:
	playerTeams.add(players[id]['team'])

teams = storage['teams']
delete = []

for id in teams:
	if not id in playerTeams:
		delete.append(id)

print(f'Games to delete ({len(delete)}):')
print(delete)

for id in delete:
	del teams[id]






print("After: {} teams, {} players and {} games.".format(
	len(storage['teams']),
	len(storage['players']),
	len(storage['games'])
))

val = ''
while not (val in ['yes', 'no']):
	val = input('Are you sure you want to proceed? (yes/no) ')

if (val == 'no'):
	exit()

print('Writing...')
syncDB()
