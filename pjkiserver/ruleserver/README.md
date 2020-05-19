Ruleserver
==========

Responsible for all game-specific logic

## Interface

### State check

To be called at game creation to verify state integrity
```python
def ruleServer.stateCheck(
    state           # current game.state dict (including FEN)
    ):
    return
        valid,      # boolean validity
        gameEnd,    # Dict <None> | { type: String [ win | draw | 50Move | repState ],
                    #                 winner: String [ playerA | playerB | draw ] }
        reason      # String (error) message for player if state rejected
```

### Move check

To be called on each move to verify rule compliance and calculate resulting
state and conditions
```python
def ruleServer.moveCheck(
    moveEvent,      # Dict, see game.events. ONLY { player, details: {move} }!
                    # By reference! Ruleserver adds details.postFEN!
    state           # game.state object _before_ move
                    # By reference! Rulserver changes fen, boardHashMap, winner if necessary!
    ):
    return
        valid,      # boolean validity
        gameEnd,    # Dict <None> | { type: String [ win | draw | 50Move | repState ],
                    #                 winner: String [ playerA | playerB | draw ] }
        reason      # String (error) message for player if move rejected
```
