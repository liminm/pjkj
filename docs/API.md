REST API
========

TOC:
- [Teams](#teams)
- [Players](#players)
- [Games](#games)
- [Events](#events)

## Allgemeine Statuscodes:

 Code				| Bedeutung
--------------------|------------------------------------------------------
 200 OK				| Default for GET
 201 Created		| Default for POST
 400 Bad request	| Syntax or format error
 401 Unauthorized	| Authorization header missing
 403 Forbidden		| Not allowed for given token's user
 404 Not found		| Resource does not exist
 409 Conflict		| Something doesn't fit (e.g. move on completed game)





## Teams

### Create Team

To participate in any game, your players need to be part of a team. For the
tournament, the ISIS group name should be given as well.

```javascript
POST /api/teams
{
  "name": "<string>",
  "isisName": "<_optional_ string>",
  "type": "jumpSturdy" || "racingKings"
}

201 CREATED
{
  "id": "<string>",
  "token": "<string>"
}
```

### Test Team Token

An enpoint to test a team token. This is entirely optional and only needed for
visual feedback in the webclient.

```javascript
GET /api/teamlogin
Authorization: Basic <teamToken>

200 OK
{
	"id": "<string teamID>",
	"valid": <boolean>
}
```

### List Teams
```javascript
GET /api/teams?count=<count>&start=<start>

200 OK
{
  "totalCount": <int total number of items in collection>,
  "items": {
    "<teamID>": {
      "name": "<string>",
      "isisName": "<string>",
      "type": "jumpSturdy" || "racingKings"
    },
    ...
  }
}
```

### Get Team
```javascript
GET /api/team/<teamID>

200 OK
{
  "name": "<string>",
  "isisName": "<string>",
  "type": "jumpSturdy" || "racingKings"
}
```








## Players

(AI or Human)

### Create Player

Players are the ressources that will actually participate in games. They are
associated to teams based on the passed team authentication token.

```javascript
POST /api/players
Authorization: Basic <teamToken>
{
  "name": "<string>"
}

201 CREATED
{
  "id": "<string>",
  "token": "<string>"
}
```

### Test Player Token

An enpoint to test a player token. This is entirely optional and only needed
for visual feedback in the webclient.

```javascript
GET /api/playerlogin
Authorization: Basic <playerToken>

200 OK
{
	"id": "<string playerID>",
	"valid": <boolean>
}
```

### List Players
```javascript
GET /api/players?count=<count>&start=<start>

200 OK
{
  "totalCount": <int total number of items in collection>,
  "items": {
    "<playerID>": {
      "name": "<string>",
      "team": "<string teamID>"
    },
    ...
  }
}
```

### Get Player
```javascript
GET /api/player/<playerID>

200 OK
{
  "name": "<string>",
  "team": "<string teamID>"
}
```







## Games

### Create Game
```javascript
POST /api/games
{
  "name": "<string>",
  "type": "jumpSturdy" || "racingKings",
  "players": {
    "playerA": {
      "id": "<string playerID>",
      "timeout": <int ms>,
      "initialTimeBudget": <int ms>
    },
    "playerB": {
      "id": "<string playerID>",
      "timeout": <int ms>,
      "initialTimeBudget": <int ms>
    }
  },
  "settings": {
    "initialFEN": "<_optional_ string fen>"
  }
}

201 CREATED
{
  "id": "<string>"
}
```

### List Games
```javascript
GET /api/games?count=<count>&start=<start>&state=[planned|running|completed]

200 OK
{
  "totalCount": <int total number of items in collection>,
  "items": {
    "<id>" {
      "name": "<string>",
      "type": "jumpSturdy" || "racingKings",
      "players": {
        "playerA": {
          "name": "<string>"
        },
        "playerB": {
          "name": "<string>"
        }
      },
      "state": {
        "state": "planned" || "running" || "completed",
        "winner": "playerA" || "playerB" || "draw" || null
      }
    },
    ...
  }
}
```

### Get Game
```javascript
GET /api/game/<gameID>

200 OK
{
  "name": "<string>",
  "type": "jumpSturdy" || "racingKings",
  "players": {
    "playerA": {
      "id": "<string playerID>",
      "name": "<string>",
      "timeout": <int ms>,
      "initialTimeBudget": <int ms>,
      "timeBudget": <int ms>
    },
    "playerB": {
      "id": "<string playerID>",
      "name": "<string>",
      "timeout": <int ms>,
      "initialTimeBudget": <int ms>,
      "timeBudget": <int ms>
    }
  },
  "settings": {
    "initialFEN": "<string fen>"
  },
  "state": {
    "state": "planned" || "running" || "completed",
    "winner": "playerA" || "playerB" || "draw" || null,
    "fen": "<string>",
    "timeBudgets": {
      "playerA": <int ms>,
      "playerB": <int ms>
    }
  }
}
```








## Events

### Send Event
```javascript
POST /api/game/<gameId>/events
Authorization: Basic <playerToken>
{
  "type": "move" || "surrender",
  "details": {
    "move": "<string uci (a1b2; e7e8q; 0000)>"
  }
}

201 CREATED
{
  "valid": <boolean>,
  "reason": "<string>"
}
```

### Get past & new Events

This is the complicated part. In order to be notified of all events happening
in the game, a comet-style [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
feed is opened via this GET request and _stays open_, feeding back data in the
SSE format. This means that as soon as, say, another player makes a move, you
will be notified of that move and can start yours.

```javascript
GET /api/game/<GameId>/events

200 OK
data: {
  "type": "move" || "gameEnd" || "serverMessage",
  "player": "playerA" || "playerB" || null,
  "timestamp": "<string iso utc>",
  "details": {
    "move": "<string uci (a1b2; e7e8q; 0000)>",
    "postFEN": "<string fen after move>",
    "time": <int ms>
  } || {
    "type": "win" || "surrender" || "draw" || "timeout" || "timeBudget" || "50move" || "repState",
    "winner": "playerA" || "playerB" || "draw"
  } || {
    "messageText": "<string>"
  }
}

data: ...
```
