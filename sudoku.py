import os
import random
import copy


def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            print(board[i][j], end=" ")
        print()


def is_valid_move(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True


def solve_sudoku(board):
    def next_empty_cell(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None, None

    def solve(board):
        row, col = next_empty_cell(board)
        if row is None:
            return True

        for num in range(1, 10):
            if is_valid_move(board, row, col, num):
                board[row][col] = num
                if solve(board):
                    return True
                board[row][col] = 0

        return False

    solve(board)


def generate_puzzle(difficulty):
    full_board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(full_board)

    puzzle = copy.deepcopy(full_board)
    for _ in range(30 + difficulty * 5):
        row, col = random.randint(0, 8), random.randint(0, 8)
        puzzle[row][col] = 0

    return full_board, puzzle


def main():
    difficulty = int(
        input("Choose difficulty level (1: Easy, 2: Medium, 3: Hard): "))
    solution, board = generate_puzzle(difficulty)

    while True:
        print_board(board)
        move = input("Enter move (row, col, number): ")

        try:
            row, col, num = map(int, move.split(','))
            row -= 1
            col -= 1
        except ValueError:
            print("Invalid input. Press enter to try again.")
            input()
            continue

        if 0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9 and board[row][col] == 0:
            if solution[row][col] == num:
                board[row][col] = num
            else:
                print("Wrong move. Press enter to try again.")
                input()
        else:
            print("Invalid move. Press enter to try again.")
            input()


if __name__ == "__main__":
    main()
