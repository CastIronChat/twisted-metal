# Notes

## What we want to do

Every player has lives; when they die they lose lives.
But this is not shown to the players anywhere; it's not in the HUD

So our task is to add visual depiction of the # of lives to the HUD.

## What we talked about

`RoundController` and `GameMode` are jointly responsible for starting a round, waiting for a winner, and ending the round
`StockGameMode` is a subclass of `GameMode`

`sprite_lists` / `SpriteLists`
`update()` and `draw()` conventions

## Questions for next time

was looking thru player, player_mananager, hud, playerhud, to find references to player state but wasn't see them
lives is mentioned in stock.py
 
- `Player` objects: 4 of them
- `Hud` one of them
  - `PlayerHud`: 4 of them
    - each stores a reference to the `Player` that it visualizes
- `RoundController`
- `StockGameMode` subclass of `GameMode`
  - `StockGameModePlayerState` 4 of them, one per player
  - `EmptyGameMode`
  - `CtfGameModePlayerState` 4 of them, one per player (hypothetical)

- Option A:
  - give each `PlayerHud` access to the `StockGameModePlayerState` for its player
  - conditional logic within `PlayerHud` to detect if it's `StockGameMode`, and if yes, then show lives
  - `if isinstance(player_state, StockGameModePlayerState):`
  - isinstance explanation https://www.w3schools.com/python/ref_func_isinstance.asp

- Option B <-- go with this one:
  - Make a second Hud object per player, partner to `PlayerHud`, that displays game-mode-specific stuff
  - Per player, we have one `PlayerHud` and one `LivesHud`

# TODOs

- [ ] Add `EmptyGameMode` which is a mode where nobody every wins, everyone has infinite lives.
  - Probably, `GameMode` already does this.
  - Add a debug toggle to switch between `StockGameMode` and `EmptyGameMode`.  Add this toggle to `constants.py`
- [ ] Add `LivesHud`
  - gets access to `StockGameModePlayerState`
  - visualizes player's # of lives
  - [ ] Where/when do we create it?
  - [ ] How do we give it access to player state?
- [ ] Decide how it looks visually; we can always improve in future pull requests
  - Text: "Lives = 3" <-- try this to start, then think about tweaks over time

# Chicken and egg issue with wiring GameMode states into PlayerHud

- `self.player_manager.setup()` creates 4 players
- `game_mode = GameMode()` is created, it has access to nothing
- `round_controller = RoundController(game_mode, players)` is given access to the game mode and the players
- `for each player: player.round_controller = round_controller` each player is given access to `round_controller` so that it can notify of deaths
- `hud = Hud(players)` and `PlayerHud(player)` <-- this is where the HUD tries to figure out if it needs to visualize lives
  - at this point, it would be really nice if game mode states were already created