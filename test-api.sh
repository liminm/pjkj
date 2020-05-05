#!/bin/bash

HOST=localhost:5000

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




GAMEINFO=`echo '
{
	"name": "Finale",
	"type": "racingKings",
	"players": {
		"playerA":' \"${PLAYER1ID}\", '
		"playerB":' \"${PLAYER2ID}\" '
	},
	"settings": {
		"initialFEN": "a/b/c",
		"timeBudget": 120000,
		"timeout": "60000"
	}
}
' | http POST ${HOST}/games`

GAMEID=`echo ${GAMEINFO} | jq -r .id`

echo ${GAMEID}

http -v ${HOST}/games
http -v ${HOST}/game/${GAMEID}

http -vS --timeout=2 ${HOST}/game/${GAMEID}/events





EV1INFO=`echo '
{
	"type": "move",
	"details": {
		"move": "a1b2"
	}
}
' | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYER1TOKEN}"`

echo ${EV1INFO}

http -vS --timeout=2 ${HOST}/game/${GAMEID}/events





EV2INFO=`echo '
{
	"type": "move",
	"details": {
		"move": "b2c3"
	}
}
' | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYER2TOKEN}"`

echo ${EV2INFO}





EV3INFO=`echo '
{
	"type": "surrender"
}
' | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYER1TOKEN}"`

echo ${EV3INFO}

http -vS --timeout=2 ${HOST}/game/${GAMEID}/events
