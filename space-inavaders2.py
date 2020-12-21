import pygame
import random
import math as mt
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Space Invaders")

# assests directory
DIR_IMG = "C:/Users/User/Desktop/python/"
DIR_SOUND = "C:/Users/User/Desktop/python projects/shoting/"


# Background image
backgroundImg = pygame.image.load(DIR_IMG + "space.png")

# Background sound
mixer.music.load(DIR_SOUND+'bcsound1.mp3')
mixer.music.play(-1)


# Player
playerImg = pygame.image.load(DIR_IMG + "ship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
ENE_X = []
ENE_Y = []
ENE_X_change = []
ENE_Y_change = []
number_of_enemies = 8
enemy_MX = 0.5

# enemy fire
fireImg = []
fireX = []
fireY = []
fireX_change = []
fireY_change = []
fire_state = []
fire_MX = 0
fire_MY = 2
number_of_fires = 1
FIRES_INTERVAL = 1
ENEMY_FIRE = pygame.time.get_ticks()


# enemy respawning random coordinates
def respawn_coor_x():
    return random.randint(0, 530)


def respawn_coor_y(x):
    return random.randint(0, 20) - x


for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load(DIR_IMG + "monster2.png"))
    enemyImg[i] = pygame.transform.scale(enemyImg[i], (64, 64))

    fireImg.append(pygame.image.load(DIR_IMG + "fire.png"))
    fireImg[i] = pygame.transform.scale(fireImg[i], (24, 24))

    # random enemy coordinates
    x = respawn_coor_x()
    y = respawn_coor_y(i * 50)
    ENE_X.append(x)
    ENE_Y.append(y)
    fireX.append(x)
    fireY.append(y)
    ENE_X_change.append(enemy_MX)
    ENE_Y_change.append(35)
    fireX_change.append(fire_MX)
    fireY_change.append(fire_MY)
    fire_state.append("ready")

# Bullet
bulletImg = pygame.image.load(DIR_IMG + "bullets.png")
BL_X = 0
BL_Y = 480
BL_X_change = 0
bullet_PY = 6
bullet_S = "ready"


def show():
    screen.blit(backgroundImg, (0, 0))


def game_over_text():
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (110, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_S
    bullet_S = "fire"
    screen.blit(bulletImg, (x + 9, y + 10))


def fire_by_enemy(x, y):
    screen.blit(fireImg[0], (x + 14, y + 17))


def isCollision(ENE_X, ENE_Y, BL_X, BL_Y):
    dis = mt.sqrt((mt.pow((ENE_X - BL_X), 2)) + (mt.pow((ENE_Y - BL_Y), 2)))
    if dis < 25:
        return True
    else:
        return False


# Game loop
running = True

while running:
    show()
    clock.tick(1200)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_S == "ready":
                    bullet_sound = mixer.Sound(DIR_SOUND+'shot.mp3')
                    bullet_sound.play()
                    BL_X = playerX
                    fire_bullet(BL_X, BL_Y)
        # check if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0

    # change D
    playerX += playerX_change
    # limits
    if playerX <= 0:
        playerX = 0
    if playerX > 570:
        playerX = 570
    for i in range(number_of_enemies):
        ENE_X[i] += ENE_X_change[i]
        col = isCollision(ENE_X[i], ENE_Y[i], playerX, playerY)
        if col:
            for j in range(number_of_enemies):
                ENE_Y[j] = 2000
            game_over_text()
            break
        if ENE_Y[i] > 480:
            for j in range(number_of_enemies):
                ENE_Y[j] = 2000
            game_over_text()
            break
        # enemy limit
        if ENE_X[i] <= 0:
            ENE_X_change[i] = enemy_MX
            ENE_Y[i] += ENE_Y_change[i]
        if ENE_X[i] > 630:
            ENE_X_change[i] = -enemy_MX
            ENE_Y[i] += ENE_Y_change[i]
        collision = isCollision(ENE_X[i], ENE_Y[i], BL_X, BL_Y)
        if collision:
            BL_Y = 480
            bullet_S = "ready"
            enemy_destroy = mixer.Sound(DIR_SOUND+'expl.wav')
            enemy_destroy.play()
            ENE_X[i] = respawn_coor_x()
            ENE_Y[i] = respawn_coor_y(i * 50)
        enemy(ENE_X[i], ENE_Y[i], i)

    # check if previous bullet is out of screen/hit
    if BL_Y <= 0:
        BL_Y = 480
        bullet_S = "ready"
    # bullet movement
    if bullet_S == "fire":
        fire_bullet(BL_X, BL_Y)
        BL_Y -= bullet_PY

    if ((pygame.time.get_ticks() - ENEMY_FIRE) / 100) > FIRES_INTERVAL:
        ENEMY_FIRE = pygame.time.get_ticks()
        for i in range(number_of_fires):
            # which enemy will fire
            F_POS = random.randint(0, 4)
            if fire_state[F_POS] == "ready" and ENE_Y[F_POS] > 0:
                fireX[F_POS] = ENE_X[F_POS]
                fireY[F_POS] = ENE_Y[F_POS]
                fire_by_enemy(fireX[F_POS], fireY[F_POS])
                fire_state[F_POS] = "fire"

    for i in range(number_of_enemies):
        if fire_state[i] == "fire" and ENE_Y[i] > 0:
            fire_by_enemy(fireX[i], fireY[i])
            fireY[i] += 1
            hit_player = isCollision(playerX, playerY, fireX[i], fireY[i])
            if hit_player:
                fireY[i] = 2000
                player_killed = mixer.Sound(DIR_SOUND+"expl.wav")
                player_killed.play()
                for j in range(number_of_enemies):
                    ENE_Y[j] = 2000
                game_over_text()
                break
        if fireY[i] > 600:
            fire_state[i] = "ready"

    player(playerX, playerY)
    pygame.display.update()
