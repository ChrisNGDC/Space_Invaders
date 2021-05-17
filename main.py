import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen_background_color = (0, 0, 0)

# Background
background = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.set_volume(0.25)
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player (64x64 png)
player_image = pygame.image.load('player.png')
player_x_width = 64
player_x = screen_width / 2 - player_x_width / 2
player_y = screen_height - screen_height % player_x_width - player_x_width
player_x_change = 0
player_x_speed = 0.4

# Enemies (64x64 png)
number_of_enemies = 6
enemy_image = []
enemy_x_width = 64
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_x_speed = []
enemy_y_speed = []
enemy_explosion = mixer.Sound('explosion.wav')
enemy_explosion.set_volume(0.25)

for i in range(number_of_enemies):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, screen_width - enemy_x_width))
    enemy_y.append(random.choice([enemy_x_width, enemy_x_width * 2]))
    enemy_x_change.append(0)
    enemy_y_change.append(0)
    enemy_x_speed.append(0.3)
    enemy_y_speed.append(64)

# Bullet (32x32 png)
bullet_image = pygame.image.load('bullet.png')
bullet_x_width = 64
bullet_x = 0
bullet_y = player_y
bullet_y_speed = 0.8
bullet_ready = True
bullet_sound = mixer.Sound('laser.wav')
bullet_sound.set_volume(0.25)

# Score
score_value = 0
score_font = pygame.font.Font('batmfa__.ttf', 32)
score_text_x = 10
score_text_y = 10

# Game Over
game_over_font = pygame.font.Font('batmfa__.ttf', 64)
game_over_background = pygame.Surface((800, 600), pygame.SRCALPHA)
game_over_background.set_alpha(128)


def show_score(x, y):
    score = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    screen.blit(game_over_background, (0, 0))
    game_over_background.fill((0, 0, 0))
    game_over = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (screen_width / 4 - 32, screen_height / 2 - 32))
    show_score(screen_width / 3, screen_height / 2 + 32)


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, n):
    screen.blit(enemy_image[n], (x, y))


def bullet(x, y):
    screen.blit(bullet_image, (x, y))


def fire_bullet(x, y):
    global bullet_ready
    bullet_ready = False
    bullet(x, y)


def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))


def is_bullet_enemy_collision(x_bullet, y_bullet, x_enemy, y_enemy):
    return distance(x_bullet, y_bullet, x_enemy, y_enemy) <= 45 and x_bullet > x_enemy and y_bullet < y_enemy


def is_player_enemy_collision(y_player, y_enemy):
    return y_player == y_enemy


# Game running
running = True
game_over = False
while running:
    screen.fill(screen_background_color)
    screen.blit(background, (0, 0))
    if not game_over:
        show_score(score_text_x, score_text_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_x_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_x_speed
            if event.key == pygame.K_SPACE:
                if bullet_ready:
                    bullet_x = player_x + player_x_width / 4
                    bullet_sound.play()
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if player_x_change < 0:
                    player_x_change = 0
            if event.key == event.key == pygame.K_RIGHT:
                if player_x_change > 0:
                    player_x_change = 0

    if screen_width - player_x_width - player_x_change > player_x > - player_x_change:
        player_x += player_x_change
    player(player_x, player_y)

    for i in range(number_of_enemies):
        enemy_x_change[i] = enemy_x_speed[i]
        if screen_width - enemy_x_width - enemy_x_change[i] > enemy_x[i] > - enemy_x_change[i]:
            enemy_x[i] += enemy_x_change[i]
        else:
            enemy_x_speed[i] = - enemy_x_speed[i]
            enemy_y_change[i] = enemy_y_speed[i]
            enemy_y[i] += enemy_y_change[i]
        enemy(enemy_x[i], enemy_y[i], i)

        bullet_enemy_collision = is_bullet_enemy_collision(bullet_x, bullet_y, enemy_x[i], enemy_y[i])
        if bullet_enemy_collision:
            bullet_y = player_y
            bullet_ready = True
            enemy_x[i] = random.randint(0, screen_width - enemy_x_width)
            enemy_y[i] = random.choice([enemy_x_width, enemy_x_width * 2])
            enemy_explosion.play()
            score_value += 1

        player_enemy_collision = is_player_enemy_collision(player_y, enemy_y[i])
        if player_enemy_collision:
            for j in range(number_of_enemies):
                enemy_y[j] = 1000
            game_over = True
            game_over_text()
            break

    if not bullet_ready:
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_speed
        if bullet_y < 0:
            bullet_ready = True
            bullet_y = player_y

    pygame.display.update()
