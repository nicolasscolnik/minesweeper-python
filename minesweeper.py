"""
Minesweeper Game
================

This module implements a simple, medium‑complexity version of the classic
**Minesweeper** game using Python's built‑in `tkinter` library for the user
interface.  The game presents a 9×9 grid containing 10 hidden mines.  Players
click on cells to reveal them; if a mine is uncovered, the game ends.  If the
player reveals all non‑mine cells, they win.  Right‑clicking toggles a
flag/marker on a cell to help keep track of suspected mines.

The code is organized into two main classes: `Cell` and `Minesweeper`.

* `Cell` encapsulates state for each individual cell on the board, including
  whether it contains a mine, whether it has been revealed, whether it is
  flagged, and how many mines neighbour it.  It also stores the `tkinter`
  `Button` widget representing the cell in the UI.

* `Minesweeper` orchestrates the overall game logic: it constructs the board,
  lays out mines at random, calculates neighbour counts, manages the
  `tkinter` interface, responds to user events, and checks for win/loss
  conditions.  When the player uncovers all safe cells, a victory dialog is
  shown.  When a mine is clicked, all mines are revealed and the player
  loses.  A new game can be started immediately via the "Reiniciar" button.

This implementation aims to be self contained and easy to understand.  It
avoids external dependencies beyond Python's standard library and is
therefore suitable for educational purposes or as a starting point for
extensions.
"""

import random
import tkinter as tk
from tkinter import messagebox


class Cell:
    """Represents a single cell on the Minesweeper board."""

    def __init__(self, master: tk.Frame, row: int, col: int):
        self.master = master
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbour_mines = 0
        # Create the button representing this cell.
        # The lambda captures the current cell instance so that the event
        # handlers can act on the correct cell.
        self.button = tk.Button(
            master,
            width=2,
            height=1,
            relief="raised",
            font=("Helvetica", 12, "bold"),
        )
        self.button.grid(row=row, column=col, sticky="nsew")
        # Bind left and right click events.
        self.button.bind("<Button-1>", lambda e: master.event_generate("<<LeftClick>>", when="tail", data=self))
        self.button.bind("<Button-3>", lambda e: master.event_generate("<<RightClick>>", when="tail", data=self))

    def __repr__(self) -> str:  # pragma: no cover - debug convenience
        return f"Cell({self.row}, {self.col}, mine={self.is_mine}, revealed={self.is_revealed}, flagged={self.is_flagged}, neighbours={self.neighbour_mines})"


class Minesweeper(tk.Tk):
    """Main application class for the Minesweeper game."""

    BOARD_SIZE = 9
    NUM_MINES = 10

    def __init__(self) -> None:
        super().__init__()
        self.title("Buscaminas - Python")
        # Configure the grid so cells expand equally when the window is resized.
        for i in range(self.BOARD_SIZE):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)
        # Set up UI elements: frame for cells and restart button.
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.restart_button = tk.Button(self, text="Reiniciar", command=self.reset_game)
        self.restart_button.pack(fill="x")
        # Initialize game state.
        self.cells: list[list[Cell]] = []
        self.game_over = False
        self.create_board()
        # Bind custom events for left and right clicks at the frame level.
        self.frame.bind("<<LeftClick>>", self.handle_left_click)
        self.frame.bind("<<RightClick>>", self.handle_right_click)

    def create_board(self) -> None:
        """Create the initial board, place mines and compute neighbour counts."""
        # Clear any existing widgets/cells.
        for child in self.frame.winfo_children():
            child.destroy()
        self.cells.clear()
        # Create cell objects.
        for row in range(self.BOARD_SIZE):
            row_cells: list[Cell] = []
            for col in range(self.BOARD_SIZE):
                cell = Cell(self.frame, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        # Place mines at random positions.
        positions = [(r, c) for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE)]
        mines = random.sample(positions, k=self.NUM_MINES)
        for r, c in mines:
            self.cells[r][c].is_mine = True
        # Compute neighbour mine counts for each cell.
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if not self.cells[r][c].is_mine:
                    count = self.count_adjacent_mines(r, c)
                    self.cells[r][c].neighbour_mines = count

    def count_adjacent_mines(self, row: int, col: int) -> int:
        """Return the number of mines adjacent to the given cell."""
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in offsets:
            rr, cc = row + dr, col + dc
            if 0 <= rr < self.BOARD_SIZE and 0 <= cc < self.BOARD_SIZE:
                if self.cells[rr][cc].is_mine:
                    count += 1
        return count

    def handle_left_click(self, event: tk.Event) -> None:
        """Process a left click event on a cell.  Reveal the cell or end the game if it's a mine."""
        if self.game_over:
            return
        cell: Cell = event.data  # type: ignore[attr-defined]
        if cell.is_revealed or cell.is_flagged:
            return
        if cell.is_mine:
            self.reveal_mine(cell)
            self.game_over = True
            self.show_all_mines()
            messagebox.showinfo("Fin del juego", "¡Boom! Has encontrado una mina. Has perdido.")
            return
        self.reveal_cell(cell)
        if self.check_win():
            self.game_over = True
            messagebox.showinfo("Victoria", "¡Felicidades! Has despejado todas las celdas sin minas.")

    def handle_right_click(self, event: tk.Event) -> None:
        """Toggle the flagged state of a cell on right click."""
        if self.game_over:
            return
        cell: Cell = event.data  # type: ignore[attr-defined]
        if cell.is_revealed:
            return
        cell.is_flagged = not cell.is_flagged
        # Update button text accordingly.
        if cell.is_flagged:
            cell.button.config(text="🚩", disabledforeground="red")
        else:
            cell.button.config(text="")

    def reveal_cell(self, cell: Cell) -> None:
        """Reveal the cell.  If the cell has no adjacent mines, recursively reveal its neighbours."""
        if cell.is_revealed or cell.is_flagged:
            return
        cell.is_revealed = True
        cell.button.config(relief="sunken", state="disabled")
        if cell.neighbour_mines > 0:
            cell.button.config(text=str(cell.neighbour_mines), disabledforeground=self.number_color(cell.neighbour_mines))
            return
        # If zero adjacent mines, reveal neighbours (flood fill).
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = cell.row + dr, cell.col + dc
                if 0 <= rr < self.BOARD_SIZE and 0 <= cc < self.BOARD_SIZE:
                    neighbour = self.cells[rr][cc]
                    if not neighbour.is_revealed and not neighbour.is_mine:
                        self.reveal_cell(neighbour)

    def reveal_mine(self, cell: Cell) -> None:
        """Display the mine when clicked."""
        cell.button.config(text="💣", disabledforeground="black", relief="sunken", state="disabled")

    def show_all_mines(self) -> None:
        """Reveal all mines on the board.  Called when the player loses."""
        for row in self.cells:
            for cell in row:
                if cell.is_mine and not cell.is_revealed:
                    cell.button.config(text="💣", disabledforeground="black", relief="sunken", state="disabled")

    @staticmethod
    def number_color(number: int) -> str:
        """Return a color based on the number of adjacent mines to improve readability."""
        # Colour scheme roughly based on classic Minesweeper.
        colors = {
            1: "blue",
            2: "green",
            3: "red",
            4: "darkblue",
            5: "darkred",
            6: "turquoise",
            7: "black",
            8: "gray",
        }
        reaturn colors.get(number, "black")

    def check_win(self) -> bool:
        """Check whether the player has revealed all non‑mine cells."""
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def reset_game(self) -> None:
        """Reset the board and game state to start a new game."""
        self.game_over = False
        self.create_board()

    def run(self) -> None:
        """Start the Tkinter main loop."""
        self.mainloop()


def main() -> None:
    """Entry point for running Minesweeper from the command line."""
    game = Minesweeper()
    game.run()


if __name__ == "__main__":
    main()
