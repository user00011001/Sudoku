import os
import random
import copy
import curses


def init_colors():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)  
    curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_BLACK)  


def print_board(stdscr, board, cur_row, cur_col):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            stdscr.addstr("- - - - - - - - - - -\n")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                stdscr.addstr("| ")
            if i == cur_row and j == cur_col:
                attr = curses.A_REVERSE
            else:
                attr = curses.A_NORMAL
            if board[i][j] != 0:
                stdscr.addstr(str(board[i][j]) + ' ',
                              curses.color_pair(board[i][j]) | attr)
            else:
                stdscr.addstr("0 ", attr)
        stdscr.addstr("\n")


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


def main(stdscr):
    # Initialize curses screen
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.keypad(True)
    stdscr.clear()

    # Initialize colors
    init_colors()

    stdscr.addstr(
        0, 0, "Choose difficulty level (1: Easy, 2: Medium, 3: Hard): ")
    stdscr.refresh()
    difficulty = int(stdscr.getstr().decode())
    solution, board = generate_puzzle(difficulty)

    row, col = 0, 0

    while True:
        stdscr.clear()
        print_board(stdscr, board, row, col)
        stdscr.addstr(11, 0, f"Current position: ({row+1}, {col+1})")
        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q') or key == ord('Q'):
            break
        elif key == curses.KEY_UP and row > 0:
            row -= 1
        elif key == curses.KEY_DOWN and row < 8:
            row += 1
        elif key == curses.KEY_LEFT and col > 0:
            col -= 1
        elif key == curses.KEY_RIGHT and col < 8:
            col += 1
        elif ord('1') <= key <= ord('9'):
            num = key - ord('0')

            if board[row][col] == 0:
                if solution[row][col] == num:
                    board[row][col] = num
                else:
                    stdscr.addstr(
                        12, 0, "Wrong move. Press any key to try again.")
                    stdscr.refresh()
                    stdscr.getch()
        else:
            stdscr.addstr(12, 0, "Invalid move. Press any key to try again.")
            stdscr.refresh()
            stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)

if __name__ == "__main__":
    main()
