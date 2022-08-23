import pygame
from base_ship import Base_Ship
from enemy import Enemy
from player import Player
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

def draw_window(player, current_enemies, spaceship_bullets):
    for enemy in current_enemies:
        WIN.blit(AI_ENEMY, (enemy.x, enemy.y))
    WIN.blit(SPACESHIP, (player.x, player.y))

    spaceship_health_text = HEALTH_FONT.render(f"Health: {str(player.health)}", 1, WHITE)
    WIN.blit(spaceship_health_text, (10, (WIN_HEIGHT - spaceship_health_text.get_height() - 10)))

    for bullet in spaceship_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()

def handle_movement(keys_pressed, player):
    if keys_pressed[pygame.K_a] and player.x > 0: # Left
        player.update_location(player.x - VEL, player.y)
    if keys_pressed[pygame.K_d] and player.x < (WIN_WIDTH - SPACESHIP_WIDTH): # Right
        player.update_location(player.x + VEL, player.y)
    if keys_pressed[pygame.K_w] and player.y > 0: # Up
        player.update_location(player.x, player.y - VEL)
    if keys_pressed[pygame.K_s] and player.y < (WIN_HEIGHT - SPACESHIP_HEIGHT): # Downs
        player.update_location(player.x, player.y + VEL)


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
        ENEMY_VEL = DEFAULT_ENEMY_VEL * random.choice((-1, 1))
        if enemy.y > WIN_HEIGHT:
            enemy.update_location(enemy.x, 0)
        else:
            enemy.update_location(enemy.x, enemy.y + DEFAULT_ENEMY_VEL)
        enemy.update_location(enemy.x + ENEMY_VEL, enemy.y)

def has_hit_enemy(current_enemies, player):
    for enemy in current_enemies:
        if enemy.hitbox.colliderect(player.hitbox):
            player.health -= 1
            
def handle_enemy_count(MAX_ENEMIES, current_enemies):
    if (len(current_enemies)) < MAX_ENEMIES:
        enemy = Enemy(WIN_WIDTH/2 - SPACESHIP_WIDTH/2, SPACESHIP_HEIGHT)
        current_enemies.append(enemy)

def main():
    # Create Rect for spaceship & enemy
    player = Player(WIN_WIDTH/2 - SPACESHIP_WIDTH/2, WIN_HEIGHT - SPACESHIP_HEIGHT)
    current_enemies = []

    # Bullet list
    spaceship_bullets = []
    enemy_bullets = []

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
                    bullet = pygame.Rect(player.x + SPACESHIP_WIDTH/2 - 2, player.y - 5, 4, 10)
                    spaceship_bullets.append(bullet)
                    # PLAY bullet fire sound

            if event.type == SPACESHIP_HIT:
                player.health -= 1
                # PLAY bullet hit sound

        WIN.fill(GRAY)

        keys_pressed = pygame.key.get_pressed()

        if player.health <= 0:
            pygame.time.delay(5000)
            break

        handle_movement(keys_pressed, player)
        handle_enemy_count(MAX_ENEMIES, current_enemies)
        handle_enemy_movement(current_enemies)
        handle_bullets(spaceship_bullets, enemy_bullets, player, current_enemies)
        
        draw_window(player, current_enemies, spaceship_bullets)
        has_hit_enemy(current_enemies, player)

    main()

if __name__ == "__main__":
    main()