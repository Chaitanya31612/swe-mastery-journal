// main class calling Game

import java.util.*;
import java.io.*;

public class TicTacToe {
    public static void main(String[] args) {
        Player player1 = new Player("Chaitanya", 'X');
        Player player2 = new Player("John", 'O');

        Board board = new Board(3); // default 3 size

        Game game = new Game(board, List.of(player1, player2));
        game.start();
    }
}



// Game class
class Game {
  private Board board;
  private List<Player> players; // currently 2
  private int currentPlayerIndex;
  private Player winner;
  private boolean isGameOver;
  private Scanner scanner;

  public Game(Board board, List<Player> players) {
    this.board = board;
    this.players = players;
    this.currentPlayerIndex = 0;
    this.isGameOver = false;
    this.scanner = new Scanner(System.in);
  }

  public void start() {
    while (!isGameOver) {
      board.display();
      System.out.println("Current player: " + currentPlayer().getName() + " (" + currentPlayer().getSymbol() + ")");
      String input = takeInput();
      if (!validateInput(input)) {
        System.out.println("Invalid input. Please try again.");
        continue;
      }

      int row = getCellRow(input);
      int col = getCellCol(input);

      board.mark(row, col, currentPlayer().getSymbol());

      if (foundAWinner()) {
        board.display();
        winner = currentPlayer();
        isGameOver = true;
        System.out.println("Winner: " + winner.getName());
      } else if (isDraw()) {
        board.display();
        isGameOver = true;
        System.out.println("Draw!");
      } else {
        playerSwitch();
      }
    }
  }

  // input and validation
  private String takeInput() {
    System.out.println("Enter row,col (e.g. 0,1): ");
    return scanner.nextLine();
  }

  private boolean validateInput(String input) {
    try {
      String[] parts = input.split(",");
      if (parts.length != 2) {
        return false;
      }
      int row = Integer.parseInt(parts[0].trim());
      int col = Integer.parseInt(parts[1].trim());

      if (row < 0 || row >= board.size() || col < 0 || col >= board.size() || !board.isEmpty(row, col)) {
        return false;
      }
      return true;
    } catch (NumberFormatException e) {
      return false;
    }
  }

  private int getCellRow(String input) {
    return Integer.parseInt(input.split(",")[0].trim());
  }

  private int getCellCol(String input) {
    return Integer.parseInt(input.split(",")[1].trim());
  }

  // player logic
  private Player currentPlayer() {
    return players.get(currentPlayerIndex);
  }

  private void playerSwitch() {
    currentPlayerIndex = (currentPlayerIndex + 1) % players.size();
  }


  // game logic
  private boolean foundAWinner() {
    return board.hasWinner(currentPlayer().getSymbol());
  }

  private boolean isDraw() {
    return board.isFull() && !foundAWinner();
  }
}


// Board class
class Board {
  private char[][] cells;
  private int size;
  private int cellsFilled;

  public Board(int size) {
    cellsFilled = 0;
    this.size = size;
    cells = new char[size][size];
  }

  // size related
  public int size() {
    return size;
  }

  public boolean isEmpty(int row, int col) {
    return cells[row][col] == 0;
  }

  public boolean isFull() {
    return cellsFilled == size * size;
  }

  public void mark(int row, int col, char symbol) {
    cells[row][col] = symbol;
    cellsFilled++;
  }

  public void display() {
    // print cell indexes on top and left
    System.out.print("   ");
    for (int col = 0; col < size; col++) {
      System.out.print(col + "   ");
    }
    System.out.println();
    System.out.println("   -------------");
    for (int row = 0; row < size; row++) {
      System.out.print(row + " | ");
      for (int col = 0; col < size; col++) {
        char val = cells[row][col];
        System.out.print((val == 0 ? " " : val) + " | ");
      }
      System.out.println();
      System.out.println("   -------------");
    }
  }

  // traversal and logic related
  public boolean hasWinner(char symbol) {
    // traverse each row
    if (rowWiseWinner(symbol)) return true;

    // traverse each column
    if (colWiseWinner(symbol)) return true;

    // traverse diagonally
    if (diagWiseWinner(symbol)) return true;

    return false;
  }

  private boolean rowWiseWinner(char symbol) {
    for (int row = 0; row < size; row++) {
      boolean rowComplete = true;
      for (int col = 0; col < size; col++) {
        if (cells[row][col] != symbol) {
          rowComplete = false;
          break;
        }
      }
      if (rowComplete) return true;
    }
    return false;
  }

  private boolean colWiseWinner(char symbol) {
    for (int col = 0; col < size; col++) {
      boolean colComplete = true;
      for (int row = 0; row < size; row++) {
        if (cells[row][col] != symbol) {
          colComplete = false;
          break;
        }
      }
      if (colComplete) return true;
    }
    return false;
  }

  private boolean diagWiseWinner(char symbol) {
    // left downward (top-left to bottom-right)
    boolean diag1Complete = true;
    for (int i = 0; i < size; i++) {
      if (cells[i][i] != symbol) {
        diag1Complete = false;
        break;
      }
    }
    if (diag1Complete) return true;

    // right downward (top-right to bottom-left)
    boolean diag2Complete = true;
    for (int i = 0; i < size; i++) {
      if (cells[i][size - 1 - i] != symbol) {
        diag2Complete = false;
        break;
      }
    }
    return diag2Complete;
  }
}


// Player class
class Player {
  private String name;
  private char symbol;

  public Player(String name, char symbol) {
    this.name = name;
    this.symbol = symbol;
  }

  public String getName() {
    return name;
  }

  public char getSymbol() {
    return symbol;
  }
}
