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
- jumps_for_cell <Cell, Jump>
--
+ resolveMove(player)
+ final_cell?
```

#### Cell
```
- position
- Jump <optional>
+ has_jump?
```

#### Dice
```
- count
+ roll
```

#### Jump
```
- from
- to
```

#### Player
```
- position
+ setPosition(newPos)
```

#### Game
```
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

  MAX_TURNS = 10_000

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
      while (!winner && @turn <= MAX_TURNS) {
        roll = dice.roll
        log.append("Turn #{@turn}: #{current_player.name} rolled a #{roll}")
        resolved_position = board.resolve(current_player.position, roll)

        if resolved_position == current_player.position
          log.append("Overshoot, over to next player")
        elsif resolved_position < current_player.position
          log.append("Oops, encountered a snake")
        elsif resolved_position > current_player.position + roll
          log.append("Woah, found a ladder!")
        else
          log.append("Moved to position #{resolved_position}")
        end

        current_player.move_to(resolved_position)
        declare_winner! if board.final_cell?(resolved_position)
        @turn += 1 unless winner
      }
    end

    private

    def current_player
      players[(@turn-1) % players.size]
    end

    def declare_winner!
      @winner = current_player
    end
  end

  class Board
    def initialize(size, jumps)
      @size = size
      @jumps = jumps
    end

    def resolve(player_position, roll)
      new_pos = player_position + roll
      return player_position if new_pos > size # overshoot

      @jumps[new_pos] ? @jumps[new_pos].to : new_pos
    end

    def final_cell?(pos)
      pos == size
    end
  end

  class Dice
    def initialize(count)
      @count = count
    end

    def roll
      rand(1..6) * @count
    end
  end

  # Abstract Base class
  class Jump
    attr_reader :from, :to

    def initialize(from, to)
      @from = from
      @to = to
      validate!
    end
  end

  class Snake < Jump
    def validate!
      raise "Invalid snake, head should be > tail" unless from > to
    end
  end

  class Ladder < Jump
    def validate!
      raise "Invalid ladder, foot should be < head" unless from < to
    end
  end

  class Player
    attr_reader :name, :position

    def initialize(name, position = 0)
      @name = name
      @position = position
    end

    def move_to(new_position)
      @position = new_position
    end
  end

  class GameLog
    def initialize
      @entries = []
    end

    def append(entry)
      @entries << entry
    end

    def to_s
      @entries.join('\n')
    end
  end

  class Driver
    def self.play
      # Setup players
      player1 = Player.new("Ravi", 0)
      player2 = Player.new("Simran", 0)
      player3 = Player.new("Aisha", 0)

      players = [player1, player2, player3]

      # Setup jumps
      jumps = { 4 => Ladder.new(4, 14), 9 => Snake.new(9, 2),
                18 => Ladder.new(18, 28), 20 => Snake.new(20, 8),
                28 => Ladder.new(28, 38), 30 => Snake.new(30, 12),
                35 => Ladder.new(35, 45), 40 => Snake.new(40, 22),
                45 => Ladder.new(45, 55), 50 => Snake.new(50, 32),
                55 => Ladder.new(55, 65), 60 => Snake.new(60, 42),
                65 => Ladder.new(65, 75), 70 => Snake.new(70, 52),
                75 => Ladder.new(75, 85), 80 => Snake.new(80, 62),
                85 => Ladder.new(85, 95), 90 => Snake.new(90, 72),
                95 => Ladder.new(95, 100), 98 => Snake.new(98, 88) }

      board = Board.new(100, jumps)
      dice = Dice.new(2)
      game = Game.new(board, players, dice)
      game.play
      puts game.log.to_s
      puts "Winner: #{game.winner.name}"
    end
  end
end
```
