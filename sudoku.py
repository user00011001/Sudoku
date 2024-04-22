import random
import tkinter as tk
from tkinter import messagebox

class SudokuGame:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku")

        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solved_board = None
        self.difficulty = "Easy"

        self.create_widgets()
        self.generate_board()

    def create_widgets(self):
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                cell = tk.Entry(self.master, width=3, font=("Arial", 20), justify="center", bg="gray")
                cell.grid(row=i, column=j, padx=1, pady=1)
                cell.bind("<KeyRelease>", self.check_cell)
                row.append(cell)
                if (i + 1) % 3 == 0 and (j + 1) % 3 == 0:
                    cell.grid(padx=(1, 5), pady=(1, 5))
                elif (i + 1) % 3 == 0:
                    cell.grid(padx=1, pady=(1, 5))
                elif (j + 1) % 3 == 0:
                    cell.grid(padx=(1, 5), pady=1)
            self.cells.append(row)

        self.easy_button = tk.Button(self.master, text="Easy", command=lambda: self.set_difficulty("Easy"))
        self.easy_button.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

        self.medium_button = tk.Button(self.master, text="Medium", command=lambda: self.set_difficulty("Medium"))
        self.medium_button.grid(row=9, column=3, columnspan=3, padx=5, pady=5)

        self.hard_button = tk.Button(self.master, text="Hard", command=lambda: self.set_difficulty("Hard"))
        self.hard_button.grid(row=9, column=6, columnspan=3, padx=5, pady=5)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_board)
        self.reset_button.grid(row=10, column=0, columnspan=4, padx=5, pady=5)

        self.solve_button = tk.Button(self.master, text="Solve", command=self.solve_board)
        self.solve_button.grid(row=10, column=5, columnspan=4, padx=5, pady=5)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.generate_board()

    def generate_board(self):
        self.reset_board()
        self.generate_solution(self.board)
        self.solved_board = [row[:] for row in self.board]
        self.remove_cells()
        self.fill_board()

    def reset_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].config(bg="white", state="normal")

    def remove_cells(self):
        if self.difficulty == "Easy":
            num_remove = 30
        elif self.difficulty == "Medium":
            num_remove = 40
        else:
            num_remove = 50

        while num_remove > 0:
            i, j = random.randint(0, 8), random.randint(0, 8)
            if self.board[i][j] != 0:
                self.board[i][j] = 0
                num_remove -= 1

    def fill_board(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(self.board[i][j]))
                    self.cells[i][j].config(state="readonly")
                else:
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].config(state="normal", bg="gray")

    def generate_solution(self, board):
        numbers = list(range(1, 10))
        random.shuffle(numbers)

        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for num in numbers:
            if self.valid(board, num, (row, col)):
                board[row][col] = num

                if self.generate_solution(board):
                    return True

                board[row][col] = 0

        return False

    def valid(self, board, num, pos):
        # Check row
        for i in range(len(board[0])):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(board)):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return i, j

        return None

    def solve_board(self):
        if self.solved_board is None:
            messagebox.showinfo("No Solution", "The current board has no solution.")
        else:
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(self.solved_board[i][j]))
                    self.cells[i][j].config(bg="green", state="readonly")

    def check_cell(self, event):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j] == event.widget:
                    if event.widget.get() == str(self.solved_board[i][j]):
                        event.widget.config(bg="green")
                    elif event.widget.get() != "":
                        event.widget.config(bg="red")
                    else:
                        event.widget.config(bg="gray")

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()
