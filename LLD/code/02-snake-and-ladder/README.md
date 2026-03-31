# 🐍🪜 Problem 02: Snake and Ladder

> **Frequency:** 🔴 P0 | **Time:** 90 min | **Difficulty:** ⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. Board of size **N x N** (typically 10x10 = 100 cells)
2. Multiple **players** take turns
3. **Dice** roll determines movement (1-6)
4. **Snakes** move player DOWN (head → tail)
5. **Ladders** move player UP (bottom → top)
6. Player must land **exactly on 100** to win (or configurable)
7. Game ends when a player reaches the last cell

### Nice-to-Have (Extensions)
- Multiple dice
- Crooked dice (always returns a specific number — for testing)
- Multiple snakes/ladders with no overlap
- Undo last move

---

## 🧩 Key Entities

```
Game, Board, Player, Dice, Snake, Ladder, Cell
```

## 🏗️ Class Diagram

```
┌──────────────┐     ┌───────────┐     ┌──────────┐
│     Game     │1──1│   Board   │1──*│   Cell   │
├──────────────┤     ├───────────┤     ├──────────┤
│ -players     │     │ -cells    │     │ -position│
│ -board       │     │ -snakes   │     │ -snake   │
│ -dice        │     │ -ladders  │     │ -ladder  │
│ -currentTurn │     ├───────────┤     └──────────┘
├──────────────┤     │+getCell() │
│ +play()      │     └───────────┘     ┌──────────┐
│ +isOver()    │                       │  Player  │
└──────────────┘     ┌───────────┐     ├──────────┤
                     │   Dice    │     │ -name    │
                     ├───────────┤     │ -position│
                     │ -count    │     └──────────┘
                     ├───────────┤
                     │ +roll()   │     ┌──────────┐
                     └───────────┘     │  Snake   │
                                       ├──────────┤
                     ┌───────────┐     │ -head    │
                     │  Ladder   │     │ -tail    │
                     ├───────────┤     └──────────┘
                     │ -start    │
                     │ -end      │
                     └───────────┘
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Strategy** | Dice (Normal vs Crooked) | Swap dice behavior for testing |
| **Factory** | BoardFactory | Create board with different configs |

## 🔑 Key Design Decisions
- **Board composition** — Board HAS cells, cells MAY have snake or ladder (not both)
- **Game loop** — Simple turn-based: `while(!isOver()) { currentPlayer.move(dice.roll()); }`
- **Win condition** — Exact landing or overshoot handling
- **Immutability** — Snake/Ladder positions don't change after board creation

## 📁 Code Structure
```
src/
├── model/
│   ├── Board.java
│   ├── Cell.java
│   ├── Player.java
│   ├── Snake.java
│   ├── Ladder.java
│   └── Dice.java
├── Game.java
└── SnakeAndLadderDemo.java
```
