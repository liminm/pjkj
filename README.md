AI project game server
======================

This is the backend for the 2020 AI tournament at the TU Berlin AOT.

To run locally for testing, simply run these inside of the repo:
```bash
pip install -e .        # Install dependencies
sudo docker pull mongo  # Install mongoDB
sudo docker run --name mongoDB -p 27017:27017 -d mongo
python3 -m pjkiserver   # Run module
```
For more details regarding permanent installation and deployment, see
[docs/INSTALL.md](/PJ-KI/server/blob/master/docs/INSTALL.md).

The server currently provides the games "Racing Kings" and "Jump Sturdy".

Both AIs and humans on web clients connect to the same REST API, specified in
[docs/API.md](/PJ-KI/server/blob/master/docs/API.md).

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

- [Frontend](/PJ-KI/web-client)
- [Controller](/PJ-KI/server/blob/master/pjkiserver/README.md)
- [Ruleserver](/PJ-KI/server/blob/master/pjkiserver/ruleserver/README.md)
- [Storage](/PJ-KI/server/blob/master/pjkiserver/storage/README.md)
