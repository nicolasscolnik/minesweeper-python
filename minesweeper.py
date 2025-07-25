import random
import tkinter as tk
from tkinter import messagebox

# Constantes para los niveles de dificultad (tamaño, minas)
DIFFICULTY_LEVELS = {
    "Fácil": (9, 10),
    "Intermedio": (16, 40),
    "Difícil": (22, 99),
}


class Cell:
    """Representa una única celda del tablero de Buscaminas."""

    def __init__(self, master: tk.Frame, row: int, col: int) -> None:
        self.master = master
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.right_click_state = 0  # 0: Empty, 1: Flagged, 2: Question Mark
        self.neighbour_mines = 0
        self.button = tk.Button(
            master,
            width=2,
            height=1,
            relief="raised",
            font=("Helvetica", 10, "bold"),
        )
        self.button.grid(row=row, column=col)
        self.button.bind(
            "<Button-1>",
            lambda e, cell=self: master.master.handle_left_click(cell),
        )
        self.button.bind(
            "<Button-3>",
            lambda e, cell=self: master.master.handle_right_click(cell),
        )

    @property
    def is_flagged(self) -> bool:
        return self.right_click_state == 1

    @property
    def is_questioned(self) -> bool:
        return self.right_click_state == 2

    def __repr__(self) -> str:
        return (
            f"Cell({self.row}, {self.col}, mine={self.is_mine}, "
            f"revealed={self.is_revealed}, state={self.right_click_state})"
        )


class Minesweeper(tk.Tk):
    """Clase principal de la aplicación de Buscaminas con niveles y temporizador."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Buscaminas - Python")
        self.resizable(False, False)

        # --- Estado del juego ---
        self.board_size = 9
        self.num_mines = 10
        self.cells: list[list[Cell]] = []
        self.game_over = False
        self.first_click = True
        self.flags_placed = 0
        self.time_elapsed = 0
        self.timer_id = None

        # --- Creación de la Interfaz ---
        self.status_frame = tk.Frame(self, padx=10, pady=5)
        self.status_frame.pack(fill="x")

        self.mine_counter_label = tk.Label(
            self.status_frame, font=("Helvetica", 16, "bold"), width=5
        )
        self.mine_counter_label.pack(side="left")

        self.restart_button = tk.Button(
            self.status_frame,
            text="🙂",
            font=("Helvetica", 16),
            command=self.prompt_difficulty,
        )
        self.restart_button.pack(side="left", expand=True)

        self.time_label = tk.Label(
            self.status_frame, font=("Helvetica", 16, "bold"), width=5
        )
        self.time_label.pack(side="right")
        
        self.board_frame = tk.Frame(self, padx=5, pady=5)
        self.board_frame.pack()
        
        self.prompt_difficulty()

    def prompt_difficulty(self) -> None:
        """Muestra una ventana para elegir la dificultad y reiniciar el juego."""
        if self.timer_id:
            self.after_cancel(self.timer_id)
            
        dialog = tk.Toplevel(self)
        dialog.title("Nueva Partida")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Elige un nivel de dificultad:", padx=20, pady=10).pack()

        for level, (size, mines) in DIFFICULTY_LEVELS.items():
            btn = tk.Button(
                dialog,
                text=f"{level} ({size}x{size}, {mines} minas)",
                command=lambda s=size, m=mines: self.start_new_game(s, m, dialog),
            )
            btn.pack(pady=5, padx=20, fill="x")

    def start_new_game(self, size: int, mines: int, dialog: tk.Toplevel) -> None:
        """Configura e inicia una nueva partida con la dificultad elegida."""
        self.board_size = size
        self.num_mines = mines
        dialog.destroy()
        self.reset_game()

    def create_board(self) -> None:
        """Crear el tablero, colocar minas y calcular vecinos."""
        for child in self.board_frame.winfo_children():
            child.destroy()
        self.cells.clear()

        for r in range(self.board_size):
            row_cells: list[Cell] = []
            for c in range(self.board_size):
                cell = Cell(self.board_frame, r, c)
                row_cells.append(cell)
            self.cells.append(row_cells)

        mine_positions = random.sample(
            range(self.board_size * self.board_size), k=self.num_mines
        )
        for pos in mine_positions:
            r, c = divmod(pos, self.board_size)
            self.cells[r][c].is_mine = True

        for r in range(self.board_size):
            for c in range(self.board_size):
                if not self.cells[r][c].is_mine:
                    self.cells[r][c].neighbour_mines = self.count_adjacent_mines(r, c)
    
    def count_adjacent_mines(self, row: int, col: int) -> int:
        """Devuelve el número de minas adyacentes a la celda dada."""
        count = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = row + dr, col + dc
                if 0 <= rr < self.board_size and 0 <= cc < self.board_size:
                    if self.cells[rr][cc].is_mine:
                        count += 1
        return count

    def handle_left_click(self, cell: Cell) -> None:
        """Procesa el clic izquierdo: revela la celda o activa el 'chording'."""
        if self.game_over or cell.is_flagged:
            return

        # --- LÓGICA DE CHORDING ---
        if cell.is_revealed and cell.neighbour_mines > 0:
            adjacent_flags = 0
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    rr, cc = cell.row + dr, cell.col + dc
                    if 0 <= rr < self.board_size and 0 <= cc < self.board_size:
                        if self.cells[rr][cc].is_flagged:
                            adjacent_flags += 1
            
            if adjacent_flags == cell.neighbour_mines:
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if dr == 0 and dc == 0:
                            continue
                        rr, cc = cell.row + dr, cell.col + dc
                        if 0 <= rr < self.board_size and 0 <= cc < self.board_size:
                            neighbor = self.cells[rr][cc]
                            # --- LA CORRECCIÓN ESTÁ AQUÍ ---
                            # Solo actuar sobre celdas no reveladas y sin bandera
                            if not neighbor.is_revealed and not neighbor.is_flagged:
                                self.handle_left_click(neighbor)
            return

        # Si el clic es en una celda no revelada, continuar con la lógica normal
        if cell.is_revealed:
            return

        if self.first_click:
            if cell.is_mine:
                self.move_mine(cell)
            self.start_timer()
            self.first_click = False

        if cell.is_mine:
            self.end_game(won=False)
            self.reveal_mine(cell)
            return

        self.reveal_cell(cell)
        if self.check_win():
            self.end_game(won=True)

    def handle_right_click(self, cell: Cell) -> None:
        """Alterna el estado de una celda con clic derecho: Vacío -> Bandera -> Interrogación -> Vacío."""
        if self.game_over or cell.is_revealed:
            return
        
        # Determine the next state
        if cell.right_click_state == 0:  # Currently empty, go to flagged
            if self.flags_placed < self.num_mines:
                cell.right_click_state = 1
                cell.button.config(text="🚩", disabledforeground="red")
                self.flags_placed += 1
            else: # If no flags left, cycle directly to question mark
                cell.right_click_state = 2
                cell.button.config(text="?", disabledforeground="blue")
        elif cell.right_click_state == 1:  # Currently flagged, go to question mark
            cell.right_click_state = 2
            cell.button.config(text="?", disabledforeground="blue")
            self.flags_placed -= 1 # Decrement flag count when moving from flag
        elif cell.right_click_state == 2:  # Currently question mark, go to empty
            cell.right_click_state = 0
            cell.button.config(text="")
        
        self.update_mine_counter()

    def reveal_cell(self, cell: Cell) -> None:
        """Revela la celda y se expande si no tiene minas vecinas."""
        if cell.is_revealed or cell.is_flagged: # Still prevent revealing flagged cells
            return
        cell.is_revealed = True
        cell.button.config(relief="sunken", state="disabled")

        # If it was a question mark, clear its text
        if cell.is_questioned:
            cell.button.config(text="")
            cell.right_click_state = 0 # Reset state to empty after revealing

        if cell.neighbour_mines > 0:
            cell.button.config(
                text=str(cell.neighbour_mines),
                disabledforeground=self.number_color(cell.neighbour_mines),
            )
        else:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    rr, cc = cell.row + dr, cell.col + dc
                    if 0 <= rr < self.board_size and 0 <= cc < self.board_size:
                        self.reveal_cell(self.cells[rr][cc])

    def reveal_mine(self, cell: Cell) -> None:
        """Muestra la mina clickeada en rojo."""
        cell.button.config(text="💣", relief="sunken", state="disabled", bg="red")
        
    def show_all_mines(self) -> None:
        """Revela todas las minas al final del juego."""
        for row in self.cells:
            for cell in row:
                if cell.is_mine and not cell.is_revealed:
                    cell.button.config(
                        text="💣", state="disabled", relief="sunken"
                    )
                if not cell.is_mine and cell.is_flagged: # If it's flagged but not a mine
                    cell.button.config(text="❌")
                elif not cell.is_mine and cell.is_questioned: # If it's questioned but not a mine
                    cell.button.config(text="") # Clear the question mark

    @staticmethod
    def number_color(number: int) -> str:
        colors = {
            1: "blue", 2: "green", 3: "red", 4: "darkblue",
            5: "darkred", 6: "turquoise", 7: "black", 8: "gray"
        }
        return colors.get(number, "black")

    def check_win(self) -> bool:
        """Comprueba si se han revelado todas las celdas no minadas."""
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
    
    def move_mine(self, cell: Cell) -> None:
        """Mueve una mina de la celda clickeada a una nueva ubicación vacía."""
        cell.is_mine = False
        while True:
            r, c = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            new_cell = self.cells[r][c]
            if not new_cell.is_mine and new_cell != cell:
                new_cell.is_mine = True
                for row_to_update in self.cells:
                    for cell_to_update in row_to_update:
                        if not cell_to_update.is_mine:
                           cell_to_update.neighbour_mines = self.count_adjacent_mines(cell_to_update.row, cell_to_update.col)
                break

    def end_game(self, won: bool) -> None:
        """Finaliza el juego, detiene el temporizador y muestra el resultado."""
        self.game_over = True
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        
        self.show_all_mines()
        
        if won:
            self.restart_button.config(text="😎")
            messagebox.showinfo("¡Victoria!", "¡Felicidades! Has ganado la partida.")
        else:
            self.restart_button.config(text="😵")
            messagebox.showerror("¡Boom!", "Has pisado una mina. Fin del juego.")

    def reset_game(self) -> None:
        """Reinicia el tablero y el estado del juego para una nueva partida."""
        self.game_over = False
        self.first_click = True
        self.flags_placed = 0
        self.time_elapsed = 0

        self.restart_button.config(text="🙂")
        self.update_mine_counter()
        self.update_timer_label()

        # Primero, limpia y crea el nuevo tablero
        self.create_board()

        # Fuerza a Tkinter a procesar el nuevo diseño
        self.update_idletasks()
        
        # Luego, permite que la ventana se redimensione automáticamente
        # para ajustarse al nuevo tablero. Usamos '' para que se ajuste.
        self.geometry('')
    
    def update_mine_counter(self) -> None:
        """Actualiza el texto del contador de minas."""
        remaining = self.num_mines - self.flags_placed
        self.mine_counter_label.config(text=f"{remaining:03}")

    def start_timer(self) -> None:
        """Inicia el temporizador del juego."""
        if not self.game_over:
            self.time_elapsed += 1
            self.update_timer_label()
            self.timer_id = self.after(1000, self.start_timer)

    def update_timer_label(self) -> None:
        """Actualiza el texto del contador de tiempo."""
        self.time_label.config(text=f"{self.time_elapsed:03}")

def main() -> None:
    """Punto de entrada para ejecutar el Buscaminas."""
    game = Minesweeper()
    game.mainloop()

if __name__ == "__main__":
    main()