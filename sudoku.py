import os
import random
import copy
import curses


def init_colors():
    for i in range(1, 10):
        curses.init_pair(i, i, curses.COLOR_BLACK)


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


def next_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None, None


def solve_sudoku(board):
    row, col = next_empty_cell(board)
    if row is None:
        return True

    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False


def generate_puzzle(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Fill the diagonal 3x3 boxes
    for box in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board[box + i][box + j] = nums.pop()

    solve_sudoku(board)

    # Remove numbers according to difficulty
    for _ in range(30 + difficulty * 5):
        while True:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if board[row][col] != 0:
                break
        board[row][col] = 0

    solution = copy.deepcopy(board)
    solve_sudoku(solution)
    return solution, board


def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.keypad(True)
    stdscr.clear()

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
