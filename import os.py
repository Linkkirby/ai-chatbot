import pygame
import random
import sys

# ================= CONFIG =================
GRID_SIZE = 150
BLOCK = 10                  # 🔥 doubled from 5 → 10
WIDTH = HEIGHT = GRID_SIZE * BLOCK
FPS = 30

# Colors
BG = (15, 15, 15)
SNAKE_HEAD = (0, 255, 0)
SNAKE_BODY = (0, 180, 0)
FOOD_COLOR = (255, 80, 80)
TEXT_COLOR = (0, 0, 0)

# ================= INIT =================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Letters — Looping World (BIG)")
clock = pygame.time.Clock()

# 🔥 font size scales with block
font = pygame.font.SysFont("consolas", BLOCK + 4, bold=True)

# ================= GAME STATE =================
snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
direction = (0, 1)

# ================= FOOD =================
def spawn_food():
    while True:
        pos = (random.randint(0, GRID_SIZE - 1),
               random.randint(0, GRID_SIZE - 1))
        if pos not in snake:
            return pos, chr(random.randint(65, 90))

food_pos, food_char = spawn_food()

# ================= DRAW =================
def draw():
    screen.fill(BG)

    # Draw food
    fr, fc = food_pos
    letter = font.render(food_char, True, FOOD_COLOR)
    screen.blit(letter, (fc * BLOCK + 1, fr * BLOCK - 1))

    # Draw snake
    for i, (r, c) in enumerate(snake):
        rect = pygame.Rect(c * BLOCK, r * BLOCK, BLOCK, BLOCK)
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        pygame.draw.rect(screen, color, rect)

        sym = '@' if i == 0 else '#'
        text = font.render(sym, True, TEXT_COLOR)
        screen.blit(text, (c * BLOCK + 1, r * BLOCK - 1))

    pygame.display.flip()

# ================= MOVE =================
def move_snake():
    global food_pos, food_char

    dr, dc = direction
    hr, hc = snake[0]

    # 🔁 wrap around
    new_head = (
        (hr + dr) % GRID_SIZE,
        (hc + dc) % GRID_SIZE
    )

    # Self collision
    if new_head in snake:
        return False

    snake.insert(0, new_head)

    # Eat food
    if new_head == food_pos:
        food_pos, food_char = spawn_food()
    else:
        snake.pop()

    return True

# ================= MAIN LOOP =================
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in (pygame.K_w, pygame.K_UP) and direction != (1, 0):
                direction = (-1, 0)
            elif event.key in (pygame.K_s, pygame.K_DOWN) and direction != (-1, 0):
                direction = (1, 0)
            elif event.key in (pygame.K_a, pygame.K_LEFT) and direction != (0, 1):
                direction = (0, -1)
            elif event.key in (pygame.K_d, pygame.K_RIGHT) and direction != (0, -1):
                direction = (0, 1)

    if not move_snake():
        running = False

    draw()

pygame.quit()
sys.exit()
