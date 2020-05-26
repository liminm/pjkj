#!/bin/bash

HOST=localhost:5000

MODE="leaveopen"

GAMETYPE="racingKings"
MOVE1="h2h3"
MOVE2="b2b6"

#GAMETYPE="jumpSturdy"
#MOVE1="b2b3"
#MOVE2="g7g6"

function heading() {

	printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
	echo ${1}
	printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -

}

heading 'CREATING TEAM'

TEAMINFO=`printf '
{
	"name":"Team Rocket",
	"isisName":"Gruppe 7",
	"type":"%s"
}
' ${GAMETYPE} | http POST ${HOST}/teams`

echo ${TEAMINFO}

TEAMID=`echo ${TEAMINFO} | jq -r .id`
TEAMTOKEN=`echo ${TEAMINFO} | jq -r .token`

echo 'Token:' ${TEAMTOKEN}

#http -v ${HOST}/teams
http -v ${HOST}/team/${TEAMID}


heading 'CREATING PLAYER 1'

PLAYER1INFO=`echo '
{
	"name":"Oskar"
}
' | http POST ${HOST}/players "Authorization: Basic ${TEAMTOKEN}"`

echo ${PLAYER1INFO}

PLAYER1ID=`echo ${PLAYER1INFO} | jq -r .id`
PLAYER1TOKEN=`echo ${PLAYER1INFO} | jq -r .token`

echo 'Token:' ${PLAYER1TOKEN}

#http -v ${HOST}/players
http -v ${HOST}/player/${PLAYER1ID}


heading 'CREATING PLAYER 2'

PLAYER2INFO=`echo '
{
	"name":"Nicht Oskar"
}
' | http POST ${HOST}/players "Authorization: Basic ${TEAMTOKEN}"`

echo ${PLAYER2INFO}

PLAYER2ID=`echo ${PLAYER2INFO} | jq -r .id`
PLAYER2TOKEN=`echo ${PLAYER2INFO} | jq -r .token`

echo 'Token:' ${PLAYER2TOKEN}

#http -v ${HOST}/players
http -v ${HOST}/player/${PLAYER2ID}


#heading 'CHECKING PAGINATION'
#http -v "${HOST}/players?start=0&count=1"
#http -v "${HOST}/players?start=1&count=2"


heading 'CREATING GAME'

GAMEINFO=`printf '
{
	"name": "Finale",
	"type": "%s",
	"players": {
		"playerA": {
			"id": "%s",
			"timeout": 60000,
			"initialTimeBudget": 120000
		},
		"playerB": {
			"id": "%s",
			"timeout": 60000,
			"initialTimeBudget": 120000
		}
	},
	"settings": {}
}
' ${GAMETYPE} ${PLAYER1ID} ${PLAYER2ID} | http POST ${HOST}/games`

echo ${GAMEINFO}

GAMEID=`echo ${GAMEINFO} | jq -r .id`

#http -v ${HOST}/games
http -v ${HOST}/game/${GAMEID}

#http -vS --timeout=1 ${HOST}/game/${GAMEID}/events


#heading 'CHECKING FILTER'
#http -v ${HOST}/games?state=planned
#http -v ${HOST}/games?state=running
#http -v ${HOST}/games?state=completed


heading 'SENDING EVENT 1'

EV1INFO=`printf '
{
	"type": "move",
	"details": {
		"move": "%s"
	}
}
' ${MOVE1} | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYER1TOKEN}"`

echo ${EV1INFO}

#http -vS --timeout=1 ${HOST}/game/${GAMEID}/events


#heading 'CHECKING FILTER'
#http -v ${HOST}/games?state=planned
#http -v ${HOST}/games?state=running
#http -v ${HOST}/games?state=completed


heading 'SENDING EVENT 2'


EV2INFO=`printf '
{
	"type": "move",
	"details": {
		"move": "%s"
	}
}
' ${MOVE2} | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYER2TOKEN}"`

echo ${EV2INFO}


if [[ ${MODE} == "leaveopen" ]]
then
	http -vS ${HOST}/game/${GAMEID}/events
	exit 0
fi

heading 'SENDING EVENT 3'

EV3INFO=`echo '
{
	"type": "surrender"
}
' | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYER1TOKEN}"`

echo ${EV3INFO}

http -vS --timeout=1 ${HOST}/game/${GAMEID}/events


#heading 'CHECKING FILTER'
#http -v ${HOST}/games?state=planned
#http -v ${HOST}/games?state=running
#http -v ${HOST}/games?state=completed
