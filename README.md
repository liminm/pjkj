AI project game server
======================

This is the backend for the 2020 AI tournament at the TU Berlin AOT.

To run, simply call `python3 src/main.py`.

It currently provides the games "Racing Kings" and "Jump Sturdy".

Both AIs and humans on web clients connect to the same REST API, specified in
[$636](https://gitlab.tubit.tu-berlin.de/PJ-KI/server/snippets/636).

The backend is based on [Flask](https://flask.palletsprojects.com/en/1.1.x/).

# Software architechture

The entire system consists of 4 Parts:

```
+-----------------------------------------------------------+
| +------------+   +--------------------------------------+ |
| |  FRONTEND  |   |                BACKEND               | |
| |            |   | +--------------+   +---------------+ | |
| | - Views    |   | |  CONTROLLER  |   |  RULESERVER   | | |
| | - Settings |   | |              |<->|               | | |
| | - Manage   |   | | - Manage DB  |   | - Check move  | | |
| |  - Teams   |   | | - REST API   |   | - Check state | | |
| |  - Players |   | | - Combine    |   +---------------+ | |
| |  - Games   |<->| |   Everything |                     | |
| | - Play     |   | | - Time       |   +---------------+ | |
| |            |   | |   Management |   |    STORAGE    | | |
| |            |   | |              |   |               | | |
| |            |   | |              |<->| - Persistent  | | |
| |            |   | |              |   |   Database    | | |
| |            |   | +--------------+   +---------------+ | |
| +------------+   +--------------------------------------+ |
+-----------------------------------------------------------+
```

For the frontend, see the
[web-client](https://gitlab.tubit.tu-berlin.de/PJ-KI/web-client) repo.

# Controller

The controller is divided into 7 files:

- `main.py`: Flask initialization and loading of modules
- `team.py`, `player.py`, `game.py`: Endpoints and handling for those resources
- `event.py`: The event system ([SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)-Based) and related endpoints.
- `timer.py`: Timekeeping and timeout handling
- `util.py`: Various helper functions

# Storage

## How to setup Docker the first time
`sudo docker pull mongo  // just download the image
sudo docker run --name mongoDB -p 27017:27017 -d mongo // run the image`

After that MongoDB will run and not shutdown if its not explicitly told so, even after a restart it will automatically start again

To get an overview over all running container type
`sudo docker ps `


## How to use the dictionary

### How to connect to the storage module
`from storage.DatabaseDictionary import DatabaseDictionary
storage = DatabaseDictionary()`

### How to save something
`key = 'insert your key here'
game = {
    'player1': 'Lorenz',
    'player2': 'Matthias',
    'history': [
        {'FEN': '8/123/8a...', 'time_player': 1, ...},
        {'FEN': '8/123/8a...', 'time_player': 1, ...},
        ...
    ]
}
storage[key] = game`

### How to read something
`game = storage['key']`

### How to iterate over all entries
`for key in storage:
    game = storage[key]`

## Important Information
- The module only accepts String keys, if not a type error will be raised!
- The values must be convertable to json if its not there will occur errors which are not handled yet!
