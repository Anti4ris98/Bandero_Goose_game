import pygame
from pygame.constants import QUIT, K_w, K_s, K_a, K_d
import random
import os

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200
FONT = pygame.font.SysFont('Verdana', 20)
BackGround = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = BackGround.get_width()
bg_move = 2

COLOR_GREEN = (0, 255, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOUR_BLUE = (0, 0, 255)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player = pygame.transform.scale(pygame.image.load('player.png').convert_alpha(),  (100, 50))
player_rect = player.get_rect()
player_rect.center = main_display.get_rect().center


def create_bonus():
    bonus_size = (100, 200)
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (100, 200))
    bonus_rect = pygame.Rect(random.randint(50, 700), -100, *bonus_size)
    bonus_move = [0, random.randint(4, 6)]
    return [bonus, bonus_rect, bonus_move]

def create_enemy():
    enemy_size = (80, 30)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (80, 30))
    enemy_rect = pygame.Rect(WIDTH, random.randint(50, 750), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1000)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 250)

player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [6, 0]
player_move_left = [-6, 0]

enemies = []
bonuses = []
score = 0
image_index = 0

playing = True

while playing:
    FPS.tick(350)



    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])), (100, 50))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
    
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -BackGround.get_width():
        bg_X1 = BackGround.get_width()

    if bg_X2 < -BackGround.get_width():
        bg_X2 = BackGround.get_width()

    main_display.blit(BackGround, (bg_X1, 0))
    main_display.blit(BackGround, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_s] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_w] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_a] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_d] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)   

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False
         
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    main_display.blit(FONT.render(str(score), True, COLOR_RED), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))