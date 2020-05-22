#!/bin/bash

function heading() {

	printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
	echo ${1}
	printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -

}

HOST=localhost:5000

heading 'CREATING GROUP'

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


heading 'CREATING PLAYER 1'


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


heading 'CREATING PLAYER 2'


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


heading 'CHECKING PAGINATION'


http -v "${HOST}/players?start=0&count=1"
http -v "${HOST}/players?start=1&count=2"


heading 'CREATING GAME'


GAMEINFO=`echo '
{
	"name": "Finale",
	"type": "racingKings",
	"players": {
		"playerA":' \"${PLAYER1ID}\", '
		"playerB":' \"${PLAYER2ID}\" '
	},
	"settings": {
		"initialFEN": "8/8/8/8/8/8/krbnNBRK/qrbnNBRQ w - - 0 1",
		"timeBudget": 120000,
		"timeout": 60000
	}
}
' | http POST ${HOST}/games`

echo ${GAMEINFO}

GAMEID=`echo ${GAMEINFO} | jq -r .id`

echo ${GAMEID}

http -v ${HOST}/games
http -v ${HOST}/game/${GAMEID}

http -vS --timeout=1 ${HOST}/game/${GAMEID}/events


heading 'CHECKING FILTER'


http -v ${HOST}/games?state=planned
http -v ${HOST}/games?state=running
http -v ${HOST}/games?state=completed


heading 'SENDING EVENT 1'


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


heading 'CHECKING FILTER'


http -v ${HOST}/games?state=planned
http -v ${HOST}/games?state=running
http -v ${HOST}/games?state=completed


heading 'SENDING EVENT 2'


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

heading 'SENDING EVENT 3'


EV3INFO=`echo '
{
	"type": "surrender"
}
' | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYER1TOKEN}"`

echo ${EV3INFO}

http -vS --timeout=1 ${HOST}/game/${GAMEID}/events


heading 'CHECKING FILTER'


http -v ${HOST}/games?state=planned
http -v ${HOST}/games?state=running
http -v ${HOST}/games?state=completed
