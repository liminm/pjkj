#!/bin/bash

HOST=localhost:5000

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CREATING GROUP'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -

TEAMINFO=`echo '
{
	"name":"Team Rocket",
	"isisName":"Gruppe 7",
	"type":"racingKings"
}
' | http POST ${HOST}/teams`

TEAMID=`echo ${TEAMINFO} | jq -r .id`
TEAMTOKEN=`echo ${TEAMINFO} | jq -r .token`

echo ${TEAMID}
echo ${TEAMTOKEN}

http -v ${HOST}/teams
http -v ${HOST}/team/${TEAMID}


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CREATING PLAYER 1'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


PLAYER1INFO=`echo '
{
        "name":"Oskar"
}
' | http POST ${HOST}/players "Authorization: Basic ${TEAMTOKEN}"`

PLAYER1ID=`echo ${PLAYER1INFO} | jq -r .id`
PLAYER1TOKEN=`echo ${PLAYER1INFO} | jq -r .token`

echo ${PLAYER1ID}
echo ${PLAYER1TOKEN}

http -v ${HOST}/players
http -v ${HOST}/player/${PLAYER1ID}


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CREATING PLAYER 2'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


PLAYER2INFO=`echo '
{
        "name":"Nicht Oskar"
}
' | http POST ${HOST}/players "Authorization: Basic ${TEAMTOKEN}"`

PLAYER2ID=`echo ${PLAYER2INFO} | jq -r .id`
PLAYER2TOKEN=`echo ${PLAYER2INFO} | jq -r .token`

echo ${PLAYER2ID}
echo ${PLAYER2TOKEN}

http -v ${HOST}/players
http -v ${HOST}/player/${PLAYER2ID}


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CHECKING PAGINATION'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


http -v "${HOST}/players?start=0&count=1"
http -v "${HOST}/players?start=1&count=2"


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CREATING GAME'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


GAMEINFO=`echo '
{
	"name": "Finale",
	"type": "racingKings",
	"players": {
		"playerA":' \"${PLAYER1ID}\", '
		"playerB":' \"${PLAYER2ID}\" '
	},
	"settings": {
		"initialFEN": "8/8/8/8/8/8/qrbnNBRQ/krbnNBRK w - - 0 1",
		"timeBudget": 120000,
		"timeout": "60000"
	}
}
' | http POST ${HOST}/games`

GAMEID=`echo ${GAMEINFO} | jq -r .id`

echo ${GAMEID}

http -v ${HOST}/games
http -v ${HOST}/game/${GAMEID}

http -vS --timeout=1 ${HOST}/game/${GAMEID}/events


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CHECKING FILTER'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


http -v ${HOST}/games?state=planned
http -v ${HOST}/games?state=running
http -v ${HOST}/games?state=completed


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'SENDING EVENT 1'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


EV1INFO=`echo '
{
	"type": "move",
	"details": {
		"move": "h2h3"
	}
}
' | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYER1TOKEN}"`

echo ${EV1INFO}

http -vS --timeout=1 ${HOST}/game/${GAMEID}/events


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CHECKING FILTER'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


http -v ${HOST}/games?state=planned
http -v ${HOST}/games?state=running
http -v ${HOST}/games?state=completed


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'SENDING EVENT 2'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


EV2INFO=`echo '
{
	"type": "move",
	"details": {
		"move": "b2b6"
	}
}
' | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYER2TOKEN}"`

echo ${EV2INFO}

#http -vS ${HOST}/game/${GAMEID}/events
#exit 0

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'SENDING EVENT 3'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


EV3INFO=`echo '
{
	"type": "surrender"
}
' | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYER1TOKEN}"`

echo ${EV3INFO}

http -vS --timeout=1 ${HOST}/game/${GAMEID}/events


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo 'CHECKING FILTER'
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


http -v ${HOST}/games?state=planned
http -v ${HOST}/games?state=running
http -v ${HOST}/games?state=completed
