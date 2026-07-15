# Problem Statement
Design a tic-tac-toe game 

## Requirements

### Must Haves
- 3x3 grid
- played by two players
- alternate turns
- win - when column, row or diagonal is filled with the same symbol
- draw - when the board is full and no winner

### Nice to haves / Out of scope
- NxN board
- multiple rounds
- undo last move

## Entities
- Board
  is - structure with cells to play on
  knows - cell matrix and their values, board size, board empty, board full
  does - display board, update cell values, clear board

- Player
  is - entity representing a player
  knows - symbox (X or O)
  does - nothing

- Game
  is - entity representing the game
  knows - board, players, current player
  does - start game, make current player play a move, after each move check for winner or draw, end game

## Classes

```ruby
class Game
  - board: Board
  - players: Player[]
  - currentPlayer: Player
  - winner: Player
  - isOver: Boolean

  + Game(board: Board, players: Player[]): void
  + setStartingPlayer(player: Player): void
  + clearBoard(): void
  + startGame()
  + foundAWinner(): Boolean
  + isDraw(): Boolean
  + endGame(): void
  
class Board
  - cells: string[][]
  - size: number

  + Board(size: number): void
  + isFull(): Boolean
  + isEmpty(): Boolean
  + display(): void
  + updateCell(row: number, col: number, symbol: string): void

class Player
  - symbol: string
  - name: string

  + Player(symbol: string, name: string): void
  + getSymbol(): string
  + getName(): string



```
