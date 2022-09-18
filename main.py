# Notes -----------------------------------
#
# - Future ideas:
#    ○ If higher health enemies are added, instead a color for each stage (ie. low, med, high),
#      have it so that the colors are based on certain health counts (ie. high = 100-75, med = 74-25, low = 24-0)
#
# End Notes -------------------------------

import math
import pygame
from enemy import Enemy
from player import Player
import os
import random
pygame.font.init()

# Setup window
WIN_WIDTH, WIN_HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Galaga_Remake")

# Color constants
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# LOAD FONTS
ARCADE_FONT = pygame.font.Font(os.path.join("Assets", "Fonts", "ARCADECLASSIC.TTF"), 35)

# GLOBAL VARIABLES
score = 0
enemy_array_x = 0
enemy_array_y = 0
enemy_array_indices = []
is_sliding_right = True

# Variable constants
FPS = 60
VEL = 5
MAX_ENEMIES = 5
DEFAULT_ENEMY_VEL = 3
BULLET_VEL = 7
MAX_BULLETS = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
ENEMY_FIRERATE = 500
ENEMY_SPAWNRATE = 2000
ENEMY_MADRATE = 5000
ENEMY_ARRAY_SLIDE_VEL = 1
ENEMY_ARRAY_SIZE_X = math.floor(WIN_WIDTH / SPACESHIP_WIDTH - 2) # Subtract 2 so that enemies can't spawn against window max
ENEMY_ARRAY_SIZE_Y = math.floor((WIN_HEIGHT / 2) / SPACESHIP_HEIGHT - 2) # Subtract 2 so that enemies can't spawn against window max

# Custom Events
SPACESHIP_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2
ENEMY_FIRE = pygame.USEREVENT + 3
ENEMY_SPAWN = pygame.USEREVENT + 4
ENEMY_MAD = pygame.USEREVENT + 5

# load ship images
SPACESHIP = pygame.image.load(os.path.join("Assets", "Spaceship.png"))
ENEMY_LOW_IMAGE = pygame.image.load(os.path.join("Assets", "Enemy_Low.png"))
ENEMY_LOW = pygame.transform.rotate(ENEMY_LOW_IMAGE, 180)
ENEMY_MED_IMAGE = pygame.image.load(os.path.join("Assets", "Enemy_Med.png"))
ENEMY_MED = pygame.transform.rotate(ENEMY_MED_IMAGE, 180)
ENEMY_HIGH_IMAGE = pygame.image.load(os.path.join("Assets", "Enemy_High.png"))
ENEMY_HIGH = pygame.transform.rotate(ENEMY_HIGH_IMAGE, 180)

# Load Background images
background = pygame.image.load(os.path.join("Assets", "main_menu_background.png"))
background_height = background.get_height()
star_big = pygame.image.load(os.path.join("Assets", "Star_Big.png"))
star_big_height = star_big.get_height()
scroll_star_big = 0
star_small = pygame.image.load(os.path.join("Assets", "Star_Small.png"))
star_small_height = star_small.get_height()
scroll_star_small = 0

def draw_window(player, current_enemies, spaceship_bullets, enemy_array):
    # BLIT CURRENT ENEMIES
    for enemy in current_enemies:
        WIN.blit(enemy.update_image(), (enemy.location.x, enemy.location.y))
    WIN.blit(SPACESHIP, (player.x, player.y))

    # SHOW THE ENEMY'S DESIRED WAYPOINTS
    #for enemy in current_enemies:
            #for point in enemy.waypoints:
                #pygame.draw.circle(WIN, (255, 0, 0), (point[0], point[1]), 7, 0)

    # DRAW ENEMY ARRAY
    for box in enemy_array:
        pygame.draw.rect(WIN, GRAY, box, 2)

    # DRAW PLAYER'S BULLETS
    for bullet in spaceship_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    # DRAW ENEMIES' BULLETS
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
                    enemy_array_indices.append(enemy.enemy_array_index)
                    current_enemies.remove(enemy)
                    global score
                    score += 1
        if bullet.y < 0 and (bullet in spaceship_bullets):
            spaceship_bullets.remove(bullet)

    for enemy in current_enemies:
        if enemy.can_move:
            for bullet in enemy.bullets:
                bullet.y += BULLET_VEL
                if spaceship.hitbox.colliderect(bullet):
                    pygame.event.post(pygame.event.Event(SPACESHIP_HIT))
                    enemy.bullets.remove(bullet)
                elif bullet.y > WIN_HEIGHT:
                    enemy.bullets.remove(bullet)
        else:
            enemy.bullets = []

def handle_enemy_movement(current_enemies, enemy_array):
    for enemy in current_enemies:
        if enemy.can_move:
            enemy.update(enemy_array)
            enemy.update_hitbox()
        elif enemy.return_to_spawnpoint:
            enemy.return_to_spawn(enemy_array)
            enemy.update_hitbox()

def has_hit_enemy(current_enemies, player):
    for enemy in current_enemies:
        if enemy.hitbox.colliderect(player.hitbox) and enemy.canDamage:
            player.health -= 1
            enemy.canDamage = False

def handle_background():
    global scroll_star_big
    global scroll_star_small

    WIN.blit(background, (0, 0))

    # DEFINE STAR BIG/SMALL VARIABLES
    tiles_star_big = math.ceil(WIN_HEIGHT / star_big_height) + 1
    tiles_star_small = math.ceil(WIN_HEIGHT / star_small_height) + 1

    # STAR_BIG (SCROLLING)
    for i in range(0, tiles_star_big):
        WIN.blit(star_big, (0, scroll_star_big - (i * star_big_height)))

    # SCROLL STAR_BIG
    scroll_star_big += 4

    # RESET SCROLL_STAR_BIG
    if scroll_star_big > star_big_height:
        scroll_star_big = 0

    # STAR_SMALL (SCROLLING)
    for i in range(0, tiles_star_small):
        WIN.blit(star_small, (0, scroll_star_small - (i * star_small_height)))

    # SCROLL STAR_SMALL
    scroll_star_small += 2

    # RESET SCROLL_STAR_SMALL
    if scroll_star_small > star_small_height:
        scroll_star_small = 0

def create_enemy_array():
    global enemy_array_indices
    # CREATE ENEMY ARRAY
    array = []
    global ENEMY_ARRAY_SIZE_X, ENEMY_ARRAY_SIZE_Y
    box_size = 50
    for x in range(0, ENEMY_ARRAY_SIZE_X):
        for y in range(0, ENEMY_ARRAY_SIZE_Y):
            box = pygame.Rect(x * box_size + box_size, y * box_size + box_size, 50, 50) # Add box_size to offset one square off window max
            array.append(box)
    # ADD A LIST OF INDICES FOR THE ENEMY_ARRAY
    for index in range(len(array)):
        enemy_array_indices.append(index)
    return array

def handle_enemy_array_slide(enemy_array, current_enemies):
    global enemy_array_x, enemy_array_y, is_sliding_right
    enemy_array_x = enemy_array[0].x
    enemy_array_y = enemy_array[0].y


    if (enemy_array_x + (ENEMY_ARRAY_SIZE_X * SPACESHIP_WIDTH) >= WIN_WIDTH):
        is_sliding_right = False
    elif (enemy_array_x <= 0):
        is_sliding_right = True

    if (is_sliding_right):
        for spot in enemy_array:
            spot.x += ENEMY_ARRAY_SLIDE_VEL
        for enemy in current_enemies:
            if (not enemy.can_move):
                enemy.location[0] += ENEMY_ARRAY_SLIDE_VEL
                enemy.update_hitbox()
    else:
        for spot in enemy_array:
            spot.x -= ENEMY_ARRAY_SLIDE_VEL
        for enemy in current_enemies:
            if (not enemy.can_move):
                enemy.location[0] -= ENEMY_ARRAY_SLIDE_VEL
                enemy.update_hitbox()

def main():
    # CREATE RECT FOR SPACESHIP & ENEMY
    player = Player(WIN, WIN_WIDTH/2 - SPACESHIP_WIDTH/2, WIN_HEIGHT - (SPACESHIP_HEIGHT + 25))
    
    # CREATE VARIABLES
    global score
    highscore = 0
    current_enemies = []
    spaceship_bullets = []

    # GET DATA
    if os.path.exists('data.txt'):
        file = open("data.txt", "r")
        fileString = file.readlines()
        file.close()
        if fileString != '':
            for line in fileString:
                if line == '':
                    break   
                else:
                    list = line.split()
                    highscore = list[0]
    # ELSE CREATE FILE IF DATA.TXT FILE EXISTS
    else:
        file = open("data.txt", "w")
        file.close()

    # EVENT TIMER TO CALL THE ENEMY_FIRE EVENT EVERY ENEMY_FIRERATE MILLISECONDS
    pygame.time.set_timer(ENEMY_FIRE, ENEMY_FIRERATE)
    pygame.time.set_timer(ENEMY_SPAWN, ENEMY_SPAWNRATE)
    pygame.time.set_timer(ENEMY_MAD, ENEMY_MADRATE)

    enemy_array = create_enemy_array()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        handle_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(spaceship_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player.x + SPACESHIP_WIDTH/2 - 2, player.y - 5, 4, 10)
                    spaceship_bullets.append(bullet)
                    # PLAY BULLET FIRE SOUND

            if event.type == SPACESHIP_HIT:
                player.health -= 1
                # PLAY BULLET HIT SOUND

            if event.type == ENEMY_SPAWN:
                if len(current_enemies) < MAX_ENEMIES:
                    rand_array_index = random.randint(0, len(enemy_array_indices) - 1)
                    enemy = Enemy(WIN, random.randrange(0, WIN_WIDTH), 0, enemy_array, enemy_array_indices[rand_array_index])
                    enemy.return_to_spawnpoint = True
                    current_enemies.append(enemy)
                    del enemy_array_indices[rand_array_index]

            if event.type == ENEMY_FIRE:
                if len(current_enemies) == 1:
                    selectedEnemy = current_enemies[0]
                    bullet = pygame.Rect(selectedEnemy.location[0] + SPACESHIP_WIDTH/2 - 2, selectedEnemy.location[1] + SPACESHIP_HEIGHT, 4, 10)
                    selectedEnemy.bullets.append(bullet)
                if len(current_enemies) > 1:
                    randomIndex = random.randint(0, len(current_enemies) - 1)
                    selectedEnemy = current_enemies[randomIndex]
                    bullet = pygame.Rect(selectedEnemy.location[0] + SPACESHIP_WIDTH/2 - 2, selectedEnemy.location[1] + SPACESHIP_HEIGHT, 4, 10)
                    selectedEnemy.bullets.append(bullet)

            if event.type == ENEMY_MAD:
                enemy_mad = True
                if len(current_enemies) > 0:
                    for enemy in current_enemies:
                        if enemy.can_move == True:
                            enemy_mad = False
                    if enemy_mad:
                        mad_enemy = random.randint(0, len(current_enemies) -1)
                        current_enemies[mad_enemy].can_move = True

        keys_pressed = pygame.key.get_pressed()

        handle_movement(keys_pressed, player)
        handle_bullets(spaceship_bullets, player, current_enemies)
        handle_enemy_array_slide(enemy_array, current_enemies)

        handle_enemy_movement(current_enemies, enemy_array)
        has_hit_enemy(current_enemies, player)
        
        # SHOW PLAYER SCORE (NEEDED TO CREATE VARIABLE FOR RETURNED RECT OF BLIT TO GET THE X CORD)
        score_label = ARCADE_FONT.render("SCORE", True, RED)
        score_label_blit = WIN.blit(score_label, (50, -9))
        score_text = ARCADE_FONT.render(str(score), True, WHITE)
        score_text_blit = WIN.blit(score_text, (score_label_blit.x + score_label.get_width()/2 - score_text.get_width()/2, 11))
        # SHOW PLAYER HIGHSCORE (NEEDED TO CREATE VARIABLE FOR RETURNED RECT OF BLIT TO GET THE X CORD)
        highscore_label = ARCADE_FONT.render("HIGHSCORE", True, RED)
        highscore_label_blit = WIN.blit(highscore_label, (WIN_WIDTH/2 - highscore_label.get_width()/2, -9))
        highscore_text = ARCADE_FONT.render(str(highscore), True, WHITE)
        highscore_text_blit = WIN.blit(highscore_text, (highscore_label_blit.x + highscore_label.get_width()/2 - highscore_text.get_width()/2, 11))

        draw_window(player, current_enemies, spaceship_bullets, enemy_array)

        if player.health <= 0:
            pygame.time.delay(0)
            break

    # UPDATE PLAYER'S HIGHSCORE
    if int(score) > int(highscore):
        highscore = score
        file = open("data.txt", "w")
        file.write(f"{highscore}")
        file.close()
    score = 0

    # SEND TO MAIN MENU WHEN KILLED
    main_menu()

def main_menu():
    
    click = False
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        Mx, My = pygame.mouse.get_pos()

        handle_background()
        
        # PLAY BUTTON
        button_play = pygame.Rect(WIN_WIDTH/2 - 50, WIN_HEIGHT/2 - 20, 100, 40)
        play_text = pygame.font.Font.render(ARCADE_FONT, "Play", True, WHITE)
        pygame.draw.rect(WIN, RED, button_play)
        WIN.blit(play_text, (button_play.x + (button_play.width - play_text.get_width())/2, button_play.y - (play_text.get_height() - button_play.height)))

        if button_play.collidepoint(Mx, My):
            if click:
                main()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            mouse_buttons = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons[0]:
                click = True


        pygame.display.update()

if __name__ == "__main__":
    main_menu()