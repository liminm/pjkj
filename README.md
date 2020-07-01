AI project game server
======================

This is the backend for the 2020 AI tournament at the TU Berlin AOT.

The server currently provides the games "Racing Kings" and "Jump Sturdy".

## Running locally for testing and bot development

To run locally for testing without persistence, simply run these commands
inside of the repository folder:

```bash
pip3 install -r requirements.txt    # Install dependencies
python3 -m pjkiserver               # Run module
```

If you want a persistent state across server restarts, install mongoDB as
described in the INSTALL document linked below or from docker:
```
sudo docker pull mongo
sudo docker run --name mongoDB -p 27017:27017 -d mongo
```
The next time you want to use it, just start mongoDB with
```
sudo docker start mongoDB
```
and all your precious data should be right where you left it :)

Both AIs and humans on web clients connect to the same REST API, specified in
[docs/API.md](//gitlab.tubit.tu-berlin.de/PJ-KI/server/blob/master/docs/API.md).

## (Advanced users only!) Deploying permanently on dedicated machines

For more details regarding permanent installation and deployment on servers,
see [docs/INSTALL.md](//gitlab.tubit.tu-berlin.de/PJ-KI/server/blob/master/docs/INSTALL.md).

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

For more detailed information about the individual modules, see their
respective repos/folders:

- [Frontend](//gitlab.tubit.tu-berlin.de/PJ-KI/web-client)
- [Controller](//gitlab.tubit.tu-berlin.de/PJ-KI/server/blob/master/pjkiserver/README.md)
- [Ruleserver](//gitlab.tubit.tu-berlin.de/PJ-KI/server/blob/master/pjkiserver/ruleserver/README.md)
- [Storage](//gitlab.tubit.tu-berlin.de/PJ-KI/server/blob/master/pjkiserver/storage/README.md)
