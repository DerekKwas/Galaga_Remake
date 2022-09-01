# Notes -----------------------------------
#
# - Future ideas:
#    ○ If higher health enemies are added, instead a color for each stage (ie. low, med, high),
#      have it so that the colors are based on certain health counts (ie. high = 100-75, med = 74-25, low = 24-0)
#
# End Notes -------------------------------

import pygame
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
MAX_ENEMIES = 3
DEFAULT_ENEMY_VEL = 3
BULLET_VEL = 7
MAX_BULLETS = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
ENEMY_FIRERATE = 500
ENEMY_SPAWNRATE = 2000


# Custom Events
SPACESHIP_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2
ENEMY_FIRE = pygame.USEREVENT + 3
ENEMY_SPAWN = pygame.USEREVENT + 4

# load ship images
SPACESHIP = pygame.image.load(os.path.join("Assets", "Spaceship.png"))
ENEMY_LOW_IMAGE = pygame.image.load(os.path.join("Assets", "Enemy_Low.png"))
ENEMY_LOW = pygame.transform.rotate(ENEMY_LOW_IMAGE, 180)
ENEMY_MED_IMAGE = pygame.image.load(os.path.join("Assets", "Enemy_Med.png"))
ENEMY_MED = pygame.transform.rotate(ENEMY_MED_IMAGE, 180)
ENEMY_HIGH_IMAGE = pygame.image.load(os.path.join("Assets", "Enemy_High.png"))
ENEMY_HIGH = pygame.transform.rotate(ENEMY_HIGH_IMAGE, 180)

# load background image

def draw_window(player, current_enemies, spaceship_bullets):
    for enemy in current_enemies:
        WIN.blit(enemy.update_image(), (enemy.location.x, enemy.location.y))
    WIN.blit(SPACESHIP, (player.x, player.y))

    # SHOW THE ENEMY'S DESIRED WAYPOINTS
    # for enemy in current_enemies:
            # for point in enemy.waypoints:
                # pygame.draw.circle(WIN, (255, 0, 0), (point[0], point[1]), 7, 0)

    for bullet in spaceship_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    for enemy in current_enemies:
        for bullet in enemy.bullets:
            pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def handle_movement(keys_pressed, player):
    if keys_pressed[pygame.K_a] and player.x > 0: # Left
        player.update_location(player.x - VEL, player.y)
    if keys_pressed[pygame.K_d] and player.x < (WIN_WIDTH - SPACESHIP_WIDTH): # Right
        player.update_location(player.x + VEL, player.y)
    if keys_pressed[pygame.K_w] and player.y > 0: # Up
        player.update_location(player.x, player.y - VEL)
    if keys_pressed[pygame.K_s] and player.y < WIN_HEIGHT - SPACESHIP_HEIGHT: # Downs
        player.update_location(player.x, player.y + VEL)

def handle_bullets(spaceship_bullets, spaceship, current_enemies):
    for bullet in spaceship_bullets:
        bullet.y -= BULLET_VEL
        for enemy in current_enemies:
            if enemy.hitbox.colliderect(bullet) and (bullet in spaceship_bullets):
                enemy.health -= 1
                spaceship_bullets.remove(bullet)
                if enemy.health <= 0:
                    current_enemies.remove(enemy)
        if bullet.y < 0 and (bullet in spaceship_bullets):
            spaceship_bullets.remove(bullet)

    for enemy in current_enemies:
        for bullet in enemy.bullets:
            bullet.y += BULLET_VEL
            if spaceship.hitbox.colliderect(bullet):
                pygame.event.post(pygame.event.Event(SPACESHIP_HIT))
                enemy.bullets.remove(bullet)
            elif bullet.y > WIN_HEIGHT:
                enemy.bullets.remove(bullet)

def handle_enemy_movement(current_enemies):
    for enemy in current_enemies:
        enemy.update()
        enemy.update_hitbox()

def has_hit_enemy(current_enemies, player):
    for enemy in current_enemies:
        if enemy.hitbox.colliderect(player.hitbox) and enemy.canDamage:
            player.health -= 1
            enemy.canDamage = False

def handle_enemy_count(MAX_ENEMIES, current_enemies):
    if (len(current_enemies)) < MAX_ENEMIES:
        enemy = Enemy(WIN, random.randrange(0, WIN_WIDTH), SPACESHIP_HEIGHT)
        current_enemies.append(enemy)
        pygame.display.update()

# TEST
def get_random_path():
    DEFAULT_POINT = (WIN_WIDTH/2, 10)
    points = []
    pointsMax = 3
    while (len(points) <= pointsMax):
        pointsLen = len(points)
        if pointsLen == pointsMax:
            break
        elif len(points) == 0:
            points.append(DEFAULT_POINT)
        else:
            lastPoint = points[len(points) - 1]
            x = random.randint(0, WIN_WIDTH)
            y = random.randint(lastPoint[1] + 25, WIN_HEIGHT/(pointsMax - 1) * len(points))
            points.append((x,y))
        for point in points:
            pygame.draw.circle(WIN, (255, 125, 0), (point[0], point[1]), 7, 0)

def main():
    # Create Rect for spaceship & enemy
    player = Player(WIN, WIN_WIDTH/2 - SPACESHIP_WIDTH/2, WIN_HEIGHT - (SPACESHIP_HEIGHT + 25))
    current_enemies = []

    # Bullet list
    spaceship_bullets = []

    # Event timer to call the ENEMY_FIRE event every ENEMY_FIRERATE milliseconds
    pygame.time.set_timer(ENEMY_FIRE, ENEMY_FIRERATE)
    pygame.time.set_timer(ENEMY_SPAWN, ENEMY_SPAWNRATE)

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

            if event.type == ENEMY_SPAWN:
                if len(current_enemies) < MAX_ENEMIES:
                    enemy = Enemy(WIN, random.randrange(0, WIN_WIDTH), 0)
                    current_enemies.append(enemy)


            if event.type == ENEMY_FIRE:
                if len(current_enemies) > 0:
                    randomIndex = random.randint(0, len(current_enemies) - 1)
                    selectedEnemy = current_enemies[randomIndex]
                    bullet = pygame.Rect(selectedEnemy.x + SPACESHIP_WIDTH/2 - 2, selectedEnemy.y + SPACESHIP_HEIGHT, 4, 10)
                    selectedEnemy.bullets.append(bullet)

        WIN.fill(GRAY)

        keys_pressed = pygame.key.get_pressed()

        handle_movement(keys_pressed, player)
        # handle_enemy_count(MAX_ENEMIES, current_enemies)
        handle_bullets(spaceship_bullets, player, current_enemies)

        handle_enemy_movement(current_enemies)
        has_hit_enemy(current_enemies, player)
        draw_window(player, current_enemies, spaceship_bullets)

        if player.health <= 0:
            pygame.time.delay(5000)
            break

    main()

if __name__ == "__main__":
    main()