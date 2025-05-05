import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Enhanced color palette
BG_COLOR = (30, 30, 40)
SNAKE_COLOR = (50, 205, 50)
FOOD_COLOR = (255, 99, 71)
GRID_COLOR = (40, 40, 50)
OVERLAY_COLOR = (0, 0, 0, 180)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Snake and food initialization
def random_position():
    return (
        random.randrange(0, WIDTH, CELL_SIZE),
        random.randrange(0, HEIGHT, CELL_SIZE)
    )

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_snake(snake):
    for segment in snake:
        rect = pygame.Rect(*segment, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, SNAKE_COLOR, rect, border_radius=6)

def draw_food(food):
    rect = pygame.Rect(*food, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, FOOD_COLOR, rect, border_radius=8)

def show_game_over(score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    screen.blit(overlay, (0, 0))
    font_big = pygame.font.SysFont("Arial Rounded MT Bold", 48)
    font_small = pygame.font.SysFont("Arial Rounded MT Bold", 28)
    text1 = font_big.render("Game Over!", True, (255, 255, 255))
    text2 = font_small.render(f"Score: {score}", True, (255, 255, 255))
    text3 = font_small.render("Press R to Restart or Q to Quit", True, (200, 200, 200))
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 80))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 - 20))
    screen.blit(text3, (WIDTH//2 - text3.get_width()//2, HEIGHT//2 + 40))
    pygame.display.flip()

def main():
    while True:
        snake = [(WIDTH // 2, HEIGHT // 2)]
        direction = (0, -CELL_SIZE)
        food = random_position()
        score = 0
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                        direction = (0, -CELL_SIZE)
                    elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                        direction = (0, CELL_SIZE)
                    elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                        direction = (-CELL_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                        direction = (CELL_SIZE, 0)

            # Move snake
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            snake.insert(0, new_head)

            # Check for collision with food
            if new_head == food:
                score += 1
                food = random_position()
                while food in snake:
                    food = random_position()
            else:
                snake.pop()

            # Check for collision with walls or self
            if (
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake[1:]
            ):
                show_game_over(score)
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                waiting = False
                                running = False  # Restart the game
                            elif event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()
                break

            # Draw everything
            screen.fill(BG_COLOR)
            draw_grid()
            draw_snake(snake)
            draw_food(food)

            # Draw score
            font = pygame.font.SysFont("Arial Rounded MT Bold", 32)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (15, 10))

            pygame.display.flip()
            clock.tick(8)  # Slightly faster

if __name__ == "__main__":
    main()