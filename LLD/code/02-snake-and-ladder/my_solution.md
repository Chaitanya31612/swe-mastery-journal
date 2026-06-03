# Snake and Ladder Solution

## Must haves

- N*N Cells in the Board, size
- Dice, which rolls, can be multiple
- Players, multiple, which holds players positions
- Cell has optional Jump (Snake or Ladder)
- winner has to reach exactly at the final cell
- Game as orchestrator which has board, dice, players, cycles through players turns, and declare winner

#### Questions

- multiple players can be on the same postion (no)
- start policy? do player need a 6 to start (yes)

### Nice to have / Out of Scope

- multiple winners
- chain reaction

---

## Entities and Classes

- Game (Main entry point)
- Board
- Cell
- Player
- Dice
- Jump (abstract/interface) -> Snake and Ladder

## Relationships

- Game 1..1 Board 1..* Cell 1..* Jump
- Game 1..* Player
- Game 1..* Dice
- Board has the cells, map for jumps
- Cell has position, Jump
- Player has position, has_started?

#### Board

```
- size
- Cell[size]
- jumps_for_cell <Cell, Jump>
--
+ resolveMove(player)
+ final_cell?
```

```
Cell
- position
- Jump <optional>
+ has_jump?
```

```
Dice
- count
+ roll
```

```
Jump

- from
- to

```

```
Player
- position
+ setPosition(newPos)
```

```
Game

- board
- players
- dice
- log

+ play()
+ winner
```



## Code


```ruby
module SnakeAndLadder

class Game
  attr_reader :board, :players, :dice, :log, :winner
  
  def initialize(board, players, dice)
    @board = board
    @players = players
    @dice = dice
    @log = GameLog.new # has method append
    @turn = 1
  end

  def play
    while (!winner) {
      roll = dice.roll
      final_player_position = board.resolve(current_player, roll)

      puts "Overshoot, over to next player" if final_player_position == current_player.position
      current_player.move_to(final_player_position)
      declare_winner! if board.is_final_cell?(final_player_position)
      @turn++
    }

    @winner
  end

  private

  def current_player
    @players[(@turn-1) % @players.size]
  end

  def declare_winner!
    @winner = current_player
  end
end

class Board
  attr_reader :size, cells, jump_for_cell

  def initialize(size)
    @size = size
    init_cells_and_jumps(size)
  end


  
end
end
```
