import pygame
from enemy import Enemy
import os
import random
pygame.font.init()

# Setup window
WIN_WIDTH, WIN_HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Galaga_Remake")

# Color constants
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)

# Variable constants
FPS = 60
VEL = 5
MAX_ENEMIES = 5
DEFAULT_ENEMY_VEL = 3
BULLET_VEL = 7
MAX_BULLETS = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50

# Custom Events
SPACESHIP_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2

# load ship images
SPACESHIP = pygame.image.load(os.path.join("Assets", "Spaceship.png"))
AI_ENEMY_IMAGE = pygame.image.load(os.path.join("Assets", "AI_Enemy.png"))
AI_ENEMY = pygame.transform.rotate(AI_ENEMY_IMAGE, 180)


# load background image

def draw_window(spaceship, current_enemies, spaceship_bullets, enemy_bullets, spaceship_health, enemy_health):
    # WIN.blit(AI_ENEMY, (ai_enemy.x, ai_enemy.y))
    for enemy in current_enemies:
        WIN.blit(AI_ENEMY, (enemy.x, enemy.y))
    WIN.blit(SPACESHIP, (spaceship.x, spaceship.y))

    spaceship_health_text = HEALTH_FONT.render(f"Health: {str(spaceship_health)}", 1, WHITE)
    # enemy_health_text = HEALTH_FONT.render(f"Health: {enemy_health}", 1, RED)
    WIN.blit(spaceship_health_text, (10, (WIN_HEIGHT - spaceship_health_text.get_height() - 10)))
    # WIN.blit(enemy_health_text, ((WIN_WIDTH - enemy_health_text.get_width() - 10), 10))

    for bullet in spaceship_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)
    # for bullet in enemy_bullets:
        # pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def handle_movement(keys_pressed, spaceship):
    if keys_pressed[pygame.K_a] and spaceship.x > 0: # Left
        spaceship.x -= VEL
    if keys_pressed[pygame.K_d] and spaceship.x < (WIN_WIDTH - SPACESHIP_WIDTH): # Right
        spaceship.x += VEL
    if keys_pressed[pygame.K_w] and spaceship.y > 0: # Up
        spaceship.y -= VEL
    if keys_pressed[pygame.K_s] and spaceship.y < (WIN_HEIGHT - SPACESHIP_HEIGHT): # Down
        spaceship.y += VEL

def handle_bullets(spaceship_bullets, enemy_bullets, spaceship, current_enemies):
    for bullet in spaceship_bullets:
        bullet.y -= BULLET_VEL
        for enemy in current_enemies:
            if enemy.hitbox.colliderect(bullet) and (bullet in spaceship_bullets):
                enemy.health -= 1
                spaceship_bullets.remove(bullet)
                if enemy.health <= 0:
                    current_enemies.remove(enemy)
                    print("You ded son!")
        if bullet.y < 0 and (bullet in spaceship_bullets):
            spaceship_bullets.remove(bullet)

    for bullet in enemy_bullets:
        bullet.y += BULLET_VEL
        if spaceship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SPACESHIP_HIT))
            enemy_bullets.remove(bullet)
        elif bullet.y > WIN_HEIGHT:
            enemy_bullets.remove(bullet)

def handle_enemy_movement(current_enemies):
    for enemy in current_enemies:
        ENEMY_VEL = DEFAULT_ENEMY_VEL * random.choice((-5, -1, 1, 5))
        if enemy.y > WIN_HEIGHT:
            enemy.update_location(enemy.x, 0)
        else:
            enemy.update_location(enemy.x, enemy.y + DEFAULT_ENEMY_VEL)
        enemy.update_location(enemy.x + ENEMY_VEL, enemy.y)

def handle_enemy_count(MAX_ENEMIES, current_enemies):
    if (len(current_enemies)) < MAX_ENEMIES:
        enemy = Enemy(WIN_WIDTH/2 - SPACESHIP_WIDTH/2, SPACESHIP_HEIGHT)
        current_enemies.append(enemy)

def main():
    # Create Rect for spaceship & enemy
    spaceship = pygame.Rect((300 - SPACESHIP_WIDTH/2), (300 + SPACESHIP_HEIGHT/2), SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    current_enemies = []

    # Bullet list
    spaceship_bullets = []
    enemy_bullets = []
    # Player healths
    spaceship_health = 10
    enemy_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(spaceship_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(spaceship.x + SPACESHIP_WIDTH/2 - 2, spaceship.y - 5, 4, 10)
                    spaceship_bullets.append(bullet)
                    # PLAY bullet fire sound

            if event.type == SPACESHIP_HIT:
                spaceship_health -= 1
                # PLAY bullet hit sound

        WIN.fill(GRAY)

        keys_pressed = pygame.key.get_pressed()

        handle_movement(keys_pressed, spaceship)
        handle_enemy_count(MAX_ENEMIES, current_enemies)
        handle_enemy_movement(current_enemies)
        handle_bullets(spaceship_bullets, enemy_bullets, spaceship, current_enemies)

        draw_window(spaceship, current_enemies, spaceship_bullets, enemy_bullets, spaceship_health, enemy_health)

    main()

if __name__ == "__main__":
    main()