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
