import pygame
import random

pygame.init()

WINDOW_SIZE = 540
CELL_SIZE = 60
grid_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 60))
pygame.display.set_caption("Sudoku")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (60, 60, 60)
LIGHT_GRAY = (100, 100, 100)

font = pygame.font.Font(None, 36)

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

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def generate_puzzle(difficulty):
    base = 3
    side = base * base
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side
    def shuffle(s):
        return random.sample(s, len(s))
    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    squares = side * side
    empties = squares * difficulty // 10
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0
    return board

def draw_grid():
    grid_surface.fill(DARK_GRAY)
    for i in range(10):
        line_width = 4 if i % 3 == 0 else 2
        line_color = WHITE if i % 3 == 0 else GRAY
        pygame.draw.line(grid_surface, line_color, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), line_width)
        pygame.draw.line(grid_surface, line_color, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), line_width)

def draw_numbers(board, user_input, invalid_moves):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                num_color = RED if (i, j) in invalid_moves else BLUE if user_input[i][j] else WHITE
                num_surface = font.render(str(board[i][j]), True, num_color)
                grid_surface.blit(num_surface, (j * CELL_SIZE + 20, i * CELL_SIZE + 15))

def display_buttons():
    buttons = []
    labels = ["Easy", "Medium", "Hard", "Reset"]
    positions = [(50, WINDOW_SIZE + 10), (220, WINDOW_SIZE + 10), (390, WINDOW_SIZE + 10), (220, WINDOW_SIZE + 60)]
    for label, position in zip(labels, positions):
        button_rect = pygame.Rect(position[0], position[1], 100, 40)
        pygame.draw.rect(window, LIGHT_GRAY, button_rect)
        text_surface = font.render(label, True, WHITE)
        window.blit(text_surface, (position[0] + 15, position[1] + 10))
        buttons.append((button_rect, label))
    return buttons

def main():
    selected_row, selected_col = -1, -1
    difficulty = None
    board = None
    user_input = [[0 for _ in range(9)] for _ in range(9)]
    invalid_moves = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_pos = pygame.mouse.get_pos()
                if clicked_pos[1] < WINDOW_SIZE:
                    selected_col, selected_row = clicked_pos[0] // CELL_SIZE, clicked_pos[1] // CELL_SIZE
                else:
                    buttons = display_buttons()
                    for button, label in buttons:
                        if button.collidepoint(event.pos):
                            if label in ["Easy", "Medium", "Hard"]:
                                difficulty_levels = {"Easy": 3, "Medium": 4, "Hard": 5}
                                difficulty = difficulty_levels[label]
                                board = generate_puzzle(difficulty)
                                user_input = [[0 for _ in range(9)] for _ in range(9)]
                                invalid_moves = []
                            elif label == "Reset":
                                board = generate_puzzle(difficulty)
                                user_input = [[0 for _ in range(9)] for _ in range(9)]
                                invalid_moves = []
            elif event.type == pygame.KEYDOWN and board is not None and selected_row >= 0:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                elif event.key in [pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9]:
                    num = event.key - pygame.K_KP0
                elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                    board[selected_row][selected_col] = 0
                    user_input[selected_row][selected_col] = 0
                    invalid_moves = [(r, c) for r, c in invalid_moves if not (r == selected_row and c == selected_col)]
                    num = None
                else:
                    num = None

                if num is not None and (selected_row >= 0 and selected_col >= 0):
                    if board[selected_row][selected_col] == 0 or (selected_row, selected_col) in invalid_moves:
                        board[selected_row][selected_col] = num
                        user_input[selected_row][selected_col] = 1
                        if is_valid_move(board, selected_row, selected_col, num):
                            invalid_moves = [(r, c) for r, c in invalid_moves if not (r == selected_row and c == selected_col)]
                        else:
                            invalid_moves.append((selected_row, selected_col))

        window.fill(DARK_GRAY)
        draw_grid()
        if board:
            draw_numbers(board, user_input, invalid_moves)
            display_buttons()
        window.blit(grid_surface, (0, 0))
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
 
