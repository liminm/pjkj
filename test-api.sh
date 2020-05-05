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




PLAYERINFO=`echo '
{
        "name":"Oskar"
}
' | http POST ${HOST}/players "Authorization: Basic ${TEAMTOKEN}"`

PLAYERID=`echo ${PLAYERINFO} | jq -r .id`
PLAYERTOKEN=`echo ${PLAYERINFO} | jq -r .token`

echo ${PLAYERID}
echo ${PLAYERTOKEN}

http -v ${HOST}/players
http -v ${HOST}/player/${PLAYERID}




GAMEINFO=`echo '
{
	"name": "Finale",
	"type": "racingKings",
	"players": {
		"playerA":' \"${PLAYERID}\", '
		"playerB":' \"${PLAYERID}\" '
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
' | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYERTOKEN}"`

echo ${EV1INFO}

http -vS --timeout=2 ${HOST}/game/${GAMEID}/events

EV2INFO=`echo '
{
	"type": "surrender"
}
' | http POST ${HOST}/game/${GAMEID}/events "Authorization: Basic ${PLAYERTOKEN}"`

echo ${EV2INFO}

http -vS --timeout=2 ${HOST}/game/${GAMEID}/events
