import pygame
import sys

# ================= CONFIG =================
WIDTH, HEIGHT = 1000, 400
FPS = 60

BG = (30, 30, 30)
CAR_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)

# Wheel animation letters
WHEEL_FRAMES = ['|', '/', '-', '\\']

# ================= INIT =================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Letter Car Animation")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("consolas", 36, bold=True)
font_small = pygame.font.SysFont("consolas", 32, bold=True)

# ================= CAR STATE =================
car_x = -200
car_y = HEIGHT // 2
speed = 4

wheel_index = 0
wheel_timer = 0

# ================= DRAW CAR =================
def draw_car(x, y, wheel_char):
    # Car body
    body_rect = pygame.Rect(x, y, 220, 60)
    pygame.draw.rect(screen, CAR_COLOR, body_rect, border_radius=10)

    # Roof
    roof_rect = pygame.Rect(x + 40, y - 40, 140, 40)
    pygame.draw.rect(screen, CAR_COLOR, roof_rect, border_radius=10)

    # "CAR" text
    label = font_big.render("CAR", True, TEXT_COLOR)
    screen.blit(label, (x + 70, y + 15))

    # Wheels (letters)
    wheel1 = font_small.render(wheel_char, True, (255, 255, 255))
    wheel2 = font_small.render(wheel_char, True, (255, 255, 255))

    screen.blit(wheel1, (x + 35, y + 60))
    screen.blit(wheel2, (x + 165, y + 60))

# ================= MAIN LOOP =================
running = True
while running:
    clock.tick(FPS)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Move car
    car_x += speed
    if car_x > WIDTH:
        car_x = -220

    # Animate wheels
    wheel_timer += 1
    if wheel_timer % 5 == 0:
        wheel_index = (wheel_index + 1) % len(WHEEL_FRAMES)

    draw_car(car_x, car_y, WHEEL_FRAMES[wheel_index])

    pygame.display.flip()

pygame.quit()
sys.exit()
