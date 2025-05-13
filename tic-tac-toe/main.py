import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 400  # Increased height for text area
CELL_SIZE = WIDTH // 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HOVER_COLOR = (200, 200, 200)

# Load sound effects
pygame.mixer.init()
# move_sound = pygame.mixer.Sound('move.wav')
# win_sound = pygame.mixer.Sound('win.wav')

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')

# Game board
board = [['' for _ in range(3)] for _ in range(3)]

# Draw the grid
def draw_grid():
    for x in range(1, 3):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, CELL_SIZE * 3), 2)
    for y in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE), 2)

# Draw X or O with hover effect
def draw_markers():
    for y in range(3):
        for x in range(3):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if board[y][x] == 'X':
                pygame.draw.line(screen, RED, (x * CELL_SIZE + 20, y * CELL_SIZE + 20), ((x + 1) * CELL_SIZE - 20, (y + 1) * CELL_SIZE - 20), 2)
                pygame.draw.line(screen, RED, ((x + 1) * CELL_SIZE - 20, y * CELL_SIZE + 20), (x * CELL_SIZE + 20, (y + 1) * CELL_SIZE - 20), 2)
            elif board[y][x] == 'O':
                pygame.draw.circle(screen, BLUE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 20, 2)
            elif rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, HOVER_COLOR, rect)

# Draw strikethrough on the winning line
def draw_strikethrough(winning_line):
    if winning_line == 'row':
        for y in range(3):
            if all([board[y][x] == 'X' or board[y][x] == 'O' for x in range(3)]):
                pygame.draw.line(screen, BLACK, (0, y * CELL_SIZE + CELL_SIZE // 2), (WIDTH, y * CELL_SIZE + CELL_SIZE // 2), 5)
    elif winning_line == 'col':
        for x in range(3):
            if all([board[y][x] == 'X' or board[y][x] == 'O' for y in range(3)]):
                pygame.draw.line(screen, BLACK, (x * CELL_SIZE + CELL_SIZE // 2, 0), (x * CELL_SIZE + CELL_SIZE // 2, HEIGHT), 5)
    elif winning_line == 'diag1':
        pygame.draw.line(screen, BLACK, (0, 0), (WIDTH, HEIGHT), 5)
    elif winning_line == 'diag2':
        pygame.draw.line(screen, BLACK, (WIDTH, 0), (0, HEIGHT), 5)

# Check for a win and return the winning line
def check_win(player):
    for y in range(3):
        if all([board[y][x] == player for x in range(3)]):
            return 'row'
    for x in range(3):
        if all([board[y][x] == player for y in range(3)]):
            return 'col'
    if all([board[i][i] == player for i in range(3)]):
        return 'diag1'
    if all([board[i][2 - i] == player for i in range(3)]):
        return 'diag2'
    return None

# AI move
def ai_move():
    empty_cells = [(y, x) for y in range(3) for x in range(3) if board[y][x] == '']
    if empty_cells:
        y, x = random.choice(empty_cells)
        board[y][x] = 'O'

# Display game over message
def show_game_over(message):
    font = pygame.font.SysFont("Arial", 48)
    text = font.render(message, True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Main game loop
def main():
    player_turn = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                x, y = event.pos
                if y < CELL_SIZE * 3:  # Ensure clicks are within the game area
                    x //= CELL_SIZE
                    y //= CELL_SIZE
                    if board[y][x] == '':
                        board[y][x] = 'X'
                        player_turn = False
                        winning_line = check_win('X')
                        if winning_line:
                            draw_strikethrough(winning_line)
                            pygame.display.flip()
                            pygame.time.wait(1000)
                            show_game_over('Player Wins!')
                            running = False
                        elif all(board[y][x] != '' for y in range(3) for x in range(3)):
                            show_game_over('Draw!')
                            running = False

        if not player_turn and running:
            time.sleep(0.5)  # AI thinking delay
            ai_move()
            player_turn = True
            winning_line = check_win('O')
            if winning_line:
                draw_strikethrough(winning_line)
                pygame.display.flip()
                pygame.time.wait(1000)
                show_game_over('AI Wins!')
                running = False
            elif all(board[y][x] != '' for y in range(3) for x in range(3)):
                show_game_over('Draw!')
                running = False

        screen.fill(WHITE)
        draw_grid()
        draw_markers()

        # Draw text area
        pygame.draw.rect(screen, BLACK, (0, CELL_SIZE * 3, WIDTH, HEIGHT - CELL_SIZE * 3))
        font = pygame.font.SysFont("Arial", 24)
        text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, CELL_SIZE * 3 + 10))

        pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main() 