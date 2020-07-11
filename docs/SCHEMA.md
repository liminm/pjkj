Database Schema
===============

```javascript
let storage = {
    teams: {
        <id>: {
            name: String,
            isisName: String,
            type: String                    // jumpSturdy | racingKings
            token: String
        },
        ...
    },
    players: {                              // Humans and Bots
        <id>: {
            name: String,
            team: String,                   // Team ID
            token: String
        },
        ...
    },
    games: {
        <id>: {
            name: String,
            type: String,                   // jumpSturdy | racingKings
            tags: [ String ],               // List of tags like 'contest1'
            players: {
                playerA: {
                    id: String,             // Player ID
                    timeout: Int            // MilliSeconds
                    timeBudget: Int,        // MilliSeconds
                    initialTimeBudget: Int  // MilliSeconds
                },
                playerB: {
                    id: String,             // Player ID
                    timeout: Int            // MilliSeconds
                    timeBudget: Int,        // MilliSeconds
                    initialTimeBudget: Int  // MilliSeconds
                }
            },
            settings: {
                initialFEN: String,         // FEN
            },
            state: {
                state: String,              // planned | running | completed
                winner: String,             // playerA | playerB | draw | <None>
                fen: String,                // FEN
                boardHashMap: {
                    <boardHash>: Int,       // Amount of times this state occurred during game
                    ...
                }
            },
            events: [
                {
                    type: String,           // move | gameEnd | timeout | timeBudget | serverMessage
                    player: String,         // playerA | playerB | <None>
                    timestamp: String,      // ISO 8601 UTC Date String
                    details: {
                        move: String,       // [move] UCI notation a4b7
                        postFEN: String,    // [move] FEN after move
                        time: Int,          // [move] MilliSeconds
                        type: String,       // [gameEnd] surrender | win | draw | timeout | timeBudget
                        winner: String,     // [gameEnd] playerA | playerB | draw
                        timeout: Int,       // [timeout] MilliSeconds
                        timeBudget: Int,    // [timeBudget] MilliSeconds
                        messageText: String // [serverMessage]
                    }
                },
                ...
            ]
        },
        ...
    }
}
```
