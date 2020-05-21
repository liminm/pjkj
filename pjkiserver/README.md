Controller
==========

The controller is divided into 9 files:

- `__main__.py`: Flask initialization and loading of modules
- `team.py`, `player.py`, `game.py`: Endpoints and handling for those resources
- `event.py`: The event system ([SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)-Based) and related endpoints.
- `timer.py`: Timekeeping and timeout handling
- `rules.py`: Abstraction layer for ruleserver modules for different games
- `schema.py`: Data ingress format validation
- `util.py`: Various helper functions
