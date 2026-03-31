# ❌⭕ Problem 03: Tic Tac Toe

> **Frequency:** 🔴 P0 | **Time:** 90 min | **Difficulty:** ⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. **N x N board** (default 3x3)
2. Two players with distinct **symbols** (X and O)
3. Players take **turns** placing symbols
4. **Win detection** — row, column, or diagonal filled by same symbol
5. **Draw detection** — board full with no winner
6. Input **validation** — cell must be empty and within bounds

### Nice-to-Have (Extensions)
- N x N board with configurable win condition
- AI player (random or minimax)
- Undo last move
- Multiple game rounds with score tracking

---

## 🧩 Key Entities

```
Game, Board, Cell, Player, Symbol (Enum), PlayerStrategy
```

## 🏗️ Class Diagram

```
┌──────────────┐     ┌───────────┐
│     Game     │1──1│   Board   │
├──────────────┤     ├───────────┤
│ -players     │     │ -grid[][] │
│ -board       │     │ -size     │
│ -currentTurn │     ├───────────┤
├──────────────┤     │+place()   │
│ +play()      │     │+checkWin()│
│ +isOver()    │     │+isFull()  │
└──────────────┘     │+display() │
                     └───────────┘
┌──────────────┐
│    Player    │     ┌────────────────┐
├──────────────┤     │  <<interface>> │
│ -name        │     │PlayerStrategy  │
│ -symbol      │     ├────────────────┤
│ -strategy    │────>│+getMove(board) │
├──────────────┤     └───────▲────────┘
│ +makeMove()  │             ┊
└──────────────┘        ┌────┴─────┐
                        │          │
                  ┌─────┴──┐ ┌────┴────┐
                  │ Human  │ │   AI    │
                  │Strategy│ │Strategy │
                  └────────┘ └─────────┘
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Strategy** | PlayerStrategy (Human vs AI) | Different move selection |
| **Factory** | PlayerFactory | Create players by type |

## 🔑 Key Design Decisions
- **Board win check** — After each move, only check the row, col, and diagonals that the last move touched (optimization)
- **Player abstraction** — Use Strategy pattern to support Human and AI players
- **Extensibility** — N x N board with configurable K-in-a-row to win

## 📁 Code Structure
```
src/
├── model/
│   ├── Board.java
│   ├── Cell.java
│   ├── Player.java
│   └── Symbol.java
├── strategy/
│   ├── PlayerStrategy.java
│   ├── HumanStrategy.java
│   └── AIStrategy.java
├── Game.java
└── TicTacToeDemo.java
```
