# frozen_string_literal: true

# ============================================================
# PROBLEM: Snake and Ladder
# ============================================================
#
# STEP 1 == REQUIREMENT HARVEST
# ------------------------------------------------------------
# [CORE]     N x N board (default 10x10 == 100 cells)
# [CORE]     2+ players take turns in a fixed order
# [CORE]     Dice roll moves player forward by face value
# [CORE]     Snake: landing on head sends player to tail (down)
# [CORE]     Ladder: landing on bottom sends player to top (up)
# [CORE]     Exact landing on final cell to win
# [CORE]     Game ends as soon as one player wins
# [EXPECTED] Validation: snake.head > snake.tail, ladder.bottom < ladder.top
# [EXPECTED] No two jumps share the same starting cell (no overlap)
# [EXPECTED] No jump on cell 1 (start) or final cell (win)
# [EXPECTED] Pluggable dice (Strategy) so tests are deterministic
# [EXPECTED] Configurable dice count (1, 2, ... N dice summed per roll)
# [EXPECTED] Move history (game log) for replay / observability
# [OPTIONAL] Multiple winners (continue till K finish), undo last move
# [OPTIONAL] Chain jumps (land on ladder top that is a snake head)
# [TRAP]     "Animate the board" / pretty-print is presentation, not LLD
# [TRAP]     Persistence across sessions == out of scope for in-memory game
# [TRAP]     Networked multiplayer == different problem (sync, auth)
#
# ------------------------------------------------------------
# STEP 2 == CLARIFYING QUESTIONS (asked, then assumed)
# ------------------------------------------------------------
# Q: Overshoot behavior?
#    A: Stay put (most common Indian / Hasbro rule). Exact landing only.
# Q: Chain jumps allowed (snake at top of ladder, etc.)?
#    A: NO. Single jump per landing. Validate at board-build time.
# Q: Multiple players on same cell?
#    A: Allowed. No "knock back to start" rule.
# Q: Concurrency model?
#    A: Single-threaded turn loop. No locks needed. If we ever go
#       multi-process, a TurnCoordinator would own the mutex.
# Q: Scale?
#    A: 2 - 8 players, board <= 1000 cells. O(1) lookups suffice.
# Q: Who owns player position?
#    A: Player owns its position. Board is stateless wrt players.
#       Game is the only mutator (single writer principle).
# Q: What if no one ever rolls the exact number to land?
#    A: Cap at MAX_TURNS to avoid infinite loops in tests.
#
# ------------------------------------------------------------
# STEP 3 == ENTITY IDENTIFICATION
# ------------------------------------------------------------
#   Game        [Service]      orchestrator, turn loop, win check
#   Board       [Entity]       holds cells + jumps, resolves landings
#   Cell        [ValueObject]  position, optional jump (Snake/Ladder)
#   Player      [Actor]        name, position, finished?
#   Dice        [Service]      pluggable Strategy, returns 1..6 * count
#   Jump        [Entity]       abstract base: from, to
#   Snake       [Entity]       Jump where from > to
#   Ladder      [Entity]       Jump where from < to
#   GameLog     [ValueObject]  per-turn audit trail
#
# ------------------------------------------------------------
# STEP 4 == RELATIONSHIPS & RESPONSIBILITIES
# ------------------------------------------------------------
#   Game        owns -> Board, Dice, [Player], GameLog
#   Game        triggers -> turn loop, mutates Player.position
#   Board       owns -> {position => Jump} (sparse map, not Cell array)
#   Board       passive: answers "what is final position from X with roll R?"
#   Player      owns -> own position. Dumb data + finished? predicate.
#   Dice        passive: roll() returns Integer. No state beyond seed.
#   Jump        passive: knows its own from/to. No movement logic.
#
# Senior instinct: Board does NOT own Players. Players are not "on" the
# board, they have a position INDEX into the board. This keeps Board
# reusable for replay / multi-game scenarios.
#
# ------------------------------------------------------------
# STEP 5 == CLASS DIAGRAM (ASCII)
# ------------------------------------------------------------
#
#  +--------------+        +--------------+        +-------------+
#  |    Game      | 1----1 |    Board     | 1----* |    Jump     |
#  |--------------|        |--------------|        |-------------|
#  | -players     |        | -size        |        | +from       |
#  | -board       |        | -jumps{}     |        | +to         |
#  | -dice        |        |--------------|        |-------------|
#  | -log         |        | +resolve(p)  |        | <<abstract>>|
#  |--------------|        | +final_cell  |        +------+------+
#  | +play        |        +--------------+               ^
#  | +winner      |                                       |
#  +------+-------+                                +------+------+
#         |                                        |             |
#         | 1..*                                +--+--+      +---+---+
#         v                                     |Snake|      |Ladder |
#  +--------------+        +--------------+     +-----+      +-------+
#  |   Player     |        |    Dice      |
#  |--------------|        |--------------|
#  | -name        |        | -count       |
#  | -position    |        |--------------|
#  | +move(steps) |        | +roll        |  <<Strategy>>
#  +--------------+        +------+-------+
#                                 ^
#                                 |
#                       +---------+---------+
#                       |                   |
#                  +----+-----+      +------+------+
#                  | NormalDie|      | CrookedDie  |
#                  +----------+      +-------------+
#
# ------------------------------------------------------------
# STEP 6 == DESIGN DECISIONS
# ------------------------------------------------------------
# DECISION: Snake and Ladder both inherit from a Jump base
# WHY:     They are the SAME mechanic with opposite direction.
#          Resolution code becomes one line, not two branches.
# TRADEOFF: One extra class. Worth it; deletes a `case` statement.
#
# DECISION: Board stores a Hash{position => Jump}, not Array<Cell>
# WHY:     99% of cells have no jump. Sparse map is O(1) lookup
#          and avoids allocating 100 Cell objects with nil fields.
# TRADEOFF: Lose the "Cell" abstraction. Acceptable; Cell had no behavior.
#
# DECISION: Dice is a Strategy (NormalDice, CrookedDice)
# WHY:     Tests need determinism. Crooked dice == deterministic dice.
#          Also allows trick variants (loaded, weighted) without if-else.
# TRADEOFF: One extra interface. Pays for itself on first test.
#
# DECISION: Player owns its position (mutable via Game only)
# WHY:     Single-writer principle. Game is the orchestrator,
#          Player is a dumb data holder. Easy to reason about.
# TRADEOFF: Player has a setter. Mitigated by keeping it internal.
#
# DECISION: Overshoot == stay put
# WHY:     Standard rule. Matches "exact landing to win" requirement.
# TRADEOFF: Game can take many turns near the end. Bounded by MAX_TURNS.
#
# DECISION: Validate jumps at Board build time, not at resolve time
# WHY:     Fail fast. A misconfigured board is a programmer bug,
#          not a runtime condition to gracefully handle.
# TRADEOFF: Constructor does work. Acceptable; happens once.
#
# ------------------------------------------------------------
# STEP 7 == TRIPWIRES WHILE CODING
# ------------------------------------------------------------
# - Don't let Board mutate Player. Game is the only mutator.
# - Don't put movement math in Dice. Dice rolls a number, period.
# - Don't loop forever: cap MAX_TURNS in case dice never lands exact.
# - Don't allow chain jumps silently. Validate or document explicitly.
# - Don't expose @position via attr_accessor (encapsulation leak).
# - Don't conflate "position == size" (win) with "position > size" (overshoot).
# - Don't forget to validate: jump endpoints in [2, size - 1].
#
# ============================================================
# CODE BEGINS
# ============================================================

module SnakeAndLadder
  # -----------------------------------------------------------------
  # Constants. No magic numbers in the body of any class.
  # -----------------------------------------------------------------
  DEFAULT_BOARD_SIZE = 100
  DICE_FACES         = 6
  MAX_TURNS          = 10_000 # safety net for "no one ever rolls exact"

  # =================================================================
  # Dice == Strategy
  # =================================================================
  # Contract: roll() returns Integer in [count, count * DICE_FACES]
  class Dice
    attr_reader :count

    def initialize(count: 1)
      raise ArgumentError, 'dice count must be >= 1' if count < 1

      @count = count
    end

    def roll
      raise NotImplementedError
    end
  end

  class NormalDice < Dice
    def roll
      Array.new(@count) { rand(1..DICE_FACES) }.sum
    end
  end

  # Deterministic dice for tests. Cycles through a pre-set sequence.
  class CrookedDice < Dice
    def initialize(sequence:)
      super(count: 1)
      raise ArgumentError, 'sequence cannot be empty' if sequence.empty?

      @sequence = sequence
      @index    = 0
    end

    def roll
      value = @sequence[@index % @sequence.length]
      @index += 1
      value
    end
  end

  # =================================================================
  # Jump == abstract base for Snake and Ladder
  # =================================================================
  # Why a base class: resolution logic becomes Board#jump_for(pos).to
  # regardless of direction. No `case` on type at the call site.
  class Jump
    attr_reader :from, :to

    def initialize(from:, to:)
      @from = from
      @to   = to
      validate!
    end

    private

    def validate!
      raise NotImplementedError
    end
  end

  class Snake < Jump
    private

    def validate!
      raise ArgumentError, "snake head (#{@from}) must be > tail (#{@to})" if @from <= @to
    end
  end

  class Ladder < Jump
    private

    def validate!
      raise ArgumentError, "ladder bottom (#{@from}) must be < top (#{@to})" if @from >= @to
    end
  end

  # =================================================================
  # Board == passive resolver of "where does this position lead?"
  # =================================================================
  # Stores a sparse Hash of jumps. Validates the whole config at build.
  class Board
    attr_reader :size

    def initialize(size: DEFAULT_BOARD_SIZE, jumps: [])
      raise ArgumentError, 'board size must be >= 4' if size < 4

      @size  = size
      @jumps = index_jumps(jumps)
    end

    # Given a landing position, return the *final* position after any jump.
    # Single jump per landing. Chain jumps are explicitly disallowed.
    def resolve(position)
      jump = @jumps[position]
      jump ? jump.to : position
    end

    def final_cell
      @size
    end

    private

    # ---- jump indexing & validation ---------------------------------
    def index_jumps(jumps)
      indexed = {}
      jumps.each do |jump|
        ensure_in_bounds!(jump)
        ensure_unique_start!(indexed, jump)
        indexed[jump.from] = jump
      end
      ensure_no_chains!(indexed)
      indexed
    end

    def ensure_in_bounds!(jump)
      [jump.from, jump.to].each do |pos|
        next if pos.between?(2, @size - 1)

        raise ArgumentError, "jump endpoint #{pos} must be in [2, #{@size - 1}]"
      end
    end

    def ensure_unique_start!(indexed, jump)
      return unless indexed.key?(jump.from)

      raise ArgumentError, "duplicate jump start at cell #{jump.from}"
    end

    # A "chain" == landing on a jump's destination triggers another jump.
    # Disallowed by design; otherwise turn outcome is non-obvious.
    def ensure_no_chains!(indexed)
      indexed.each_value do |jump|
        next unless indexed.key?(jump.to)

        raise ArgumentError, "chain jump detected at cell #{jump.to}"
      end
    end
  end

  # =================================================================
  # Player == dumb data holder. Game is the only mutator.
  # =================================================================
  class Player
    attr_reader :name, :position

    def initialize(name)
      @name     = name
      @position = 0
    end

    # Package-private by convention. Game calls this; nothing else should.
    def position=(new_position)
      @position = new_position
    end

    def to_s
      "#{@name}@#{@position}"
    end
  end

  # =================================================================
  # GameLog == append-only audit trail. Useful for replay & debugging.
  # =================================================================
  class GameLog
    Entry = Struct.new(:turn, :player, :roll, :from, :landed, :final, :note, keyword_init: true)

    def initialize
      @entries = []
    end

    def record(**fields)
      @entries << Entry.new(**fields)
    end

    def each(&block)
      @entries.each(&block)
    end

    def size
      @entries.size
    end
  end

  # =================================================================
  # Game == orchestrator. The only place state changes happen.
  # =================================================================
  class Game
    attr_reader :board, :players, :dice, :log, :winner

    def initialize(players:, board: Board.new, dice: NormalDice.new)
      raise ArgumentError, 'need at least 2 players' if players.size < 2

      @players = players
      @board   = board
      @dice    = dice
      @log     = GameLog.new
      @winner  = nil
      @turn    = 0
    end

    def play
      while !over? && @turn < MAX_TURNS
        play_turn(current_player)
        @turn += 1
      end
      @winner
    end

    def over?
      !@winner.nil?
    end

    private

    # ---- turn flow ---------------------------------------------------
    def play_turn(player)
      roll          = @dice.roll
      from          = player.position
      landed, note  = attempt_move(player, roll)
      final         = @board.resolve(landed)
      apply_move(player, final)
      @log.record(turn: @turn, player: player.name, roll: roll,
                  from: from, landed: landed, final: final, note: note)
      declare_winner(player) if final == @board.final_cell
    end

    # Returns [landed_cell, note]. Note documents overshoot for the log.
    def attempt_move(player, roll)
      target = player.position + roll
      return [player.position, :overshoot] if target > @board.final_cell

      [target, :ok]
    end

    def apply_move(player, final_position)
      player.position = final_position
    end

    def declare_winner(player)
      @winner = player
    end

    # ---- turn rotation ----------------------------------------------
    def current_player
      @players[@turn % @players.size]
    end
  end
end

# ============================================================
# == DEMO ====================================================
# ============================================================
if $PROGRAM_NAME == __FILE__
  include SnakeAndLadder

  # ---- build a small board with a couple of snakes and ladders -----
  jumps = [
    Ladder.new(from: 4,  to: 25),
    Ladder.new(from: 13, to: 46),
    Ladder.new(from: 33, to: 49),
    Ladder.new(from: 50, to: 69),
    Ladder.new(from: 62, to: 81),
    Snake.new(from: 27,  to: 5),
    Snake.new(from: 40,  to: 3),
    Snake.new(from: 76,  to: 58),
    Snake.new(from: 99,  to: 41)
  ]

  board   = Board.new(size: 100, jumps: jumps)
  dice    = NormalDice.new(count: 1)
  players = [Player.new('Alice'), Player.new('Bob'), Player.new('Charlie')]
  game    = Game.new(players: players, board: board, dice: dice)

  winner = game.play

  puts "Winner: #{winner.name} in #{game.log.size} turns"
  puts '---- last 8 moves ----'
  game.log.each.to_a.last(8).each do |e|
    puts format('t=%-3d %-8s rolled=%d  %d -> %d -> %d  (%s)',
                e.turn, e.player, e.roll, e.from, e.landed, e.final, e.note)
  end

  # ---- deterministic run with a crooked dice (sanity check) --------
  # Sequence cycles per ROLL (not per player). With 2 players:
  #   t0 Test1 rolls 2 -> 2 -> ladder -> 99
  #   t1 Test2 rolls 6 -> 6
  #   t2 Test1 rolls 1 -> 99 + 1 = 100 -> WIN
  puts "\n---- crooked dice run ----"
  rigged_game = Game.new(
    players: [Player.new('Test1'), Player.new('Test2')],
    board:   Board.new(size: 100, jumps: [Ladder.new(from: 2, to: 99)]),
    dice:    CrookedDice.new(sequence: [2, 6, 1])
  )
  puts "Winner: #{rigged_game.play.name} (expected: Test1)"
end

# ============================================================
# STEP 8 == POST-SOLVE REFLECTION
# ============================================================
#
# WHAT COULD BREAK IN PRODUCTION
# ------------------------------------------------------------
# 1. Infinite loop near end of game: if the only way to win is rolling
#    exactly K and dice never returns K, game stalls. Mitigated by
#    MAX_TURNS, but a real product would want a draw / forfeit rule.
# 2. Concurrency: current design is single-threaded. If two threads
#    call play_turn on the same Game, Player.position becomes a race.
#    Fix: wrap turn loop in a Mutex, or move to actor model per game.
# 3. Bad board configs: chain jumps and cell-1 / cell-N jumps would
#    silently break gameplay. Caught at build time here, but a config
#    loader (YAML, DB) needs the same validation upstream.
# 4. Crooked dice in production: if CrookedDice leaks into a real game
#    via DI misconfiguration, players get a deterministic outcome.
#    Mitigation: log dice class on game start; alert on non-Normal.
# 5. Player object identity: if the same Player instance is added to
#    two games, position state corrupts. Player should be game-scoped
#    or made immutable with a separate PlayerState lookup.
#
# WHAT A GREAT FOLLOW-UP QUESTION LOOKS LIKE
# ------------------------------------------------------------
# Q: "Why didn't you make Snake and Ladder a single Jump class with
#    a sign on `to - from`?"
# A: Could have. Two classes give better readability at construction
#    sites and let validation differ per type. If we had 5+ jump
#    variants, I'd revisit and use a single class with a kind enum.
#
# Q: "How would you support 'roll a 6 to start' rule?"
# A: Add a TurnPolicy strategy. Game asks policy.can_move?(player, roll)
#    before applying. Default policy is permissive; StartOnSixPolicy
#    blocks until first 6. No change to Board / Player / Dice.
#
# Q: "What if the board has 1000s of cells with 100s of jumps?"
# A: Hash lookup is still O(1). Real concern is GameLog growing
#    unbounded. Add a ring buffer or stream-to-disk strategy. Also
#    consider sharding multi-game state behind a GameRegistry.
#
# HOW TO EXTEND THIS DESIGN
# ------------------------------------------------------------
# - Multiple dice / weighted dice: trivially absorbed by Dice strategy.
#   Just a new subclass. Game / Board / Player untouched.
# - Variant rules (knock-out, bonus turn on 6, team play): introduce a
#   RuleSet or TurnPolicy object passed to Game. Game.play_turn would
#   delegate decisions (next_player, on_landing). Player and Board
#   absorb this cleanly. Game's turn loop is the only thing that grows.
# - Persistence / replay: GameLog already exists. Make it serializable.
#   Replay == construct Board + Players, feed dice rolls from the log
#   via CrookedDice(sequence: log.map(&:roll)). Done.
# - Multiplayer over network: Game becomes server-side. Add a
#   TurnCoordinator that gates input from clients. Player gains an
#   identity (session token). Core model unchanged.
#
# ONE THING MOST PEOPLE GET WRONG ON THIS PROBLEM
# ------------------------------------------------------------
# They put movement logic on Player (`player.move(dice, board)`) so
# Player ends up depending on Dice and Board. Suddenly Player is not a
# data class, it's an orchestrator, and it knows about win conditions,
# overshoot, and jumps. The Game class becomes anemic and the design
# violates Single Responsibility.
#
# Senior move: keep Player passive. Game owns the turn algorithm.
# Board answers "where does this position land?". Dice answers "what
# number did I roll?". Each class has ONE reason to change. This is
# what lets the design absorb new rules (start-on-6, team play,
# variants) without rewriting Player.
