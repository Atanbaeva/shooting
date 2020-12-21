import pygame
import random
import math
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
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
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
time_interval_between_fires = 1 
starting_time_for_fire = pygame.time.get_ticks()


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
    enemyX.append(x)
    enemyY.append(y)
    fireX.append(x)
    fireY.append(y)
    enemyX_change.append(enemy_MX)
    enemyY_change.append(35)
    fireX_change.append(fire_MX)
    fireY_change.append(fire_MY)
    fire_state.append("ready")

# Bullet
bulletImg = pygame.image.load(DIR_IMG + "bullets.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
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


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 25:
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
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
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
        enemyX[i] += enemyX_change[i]
        col = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if col:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        if enemyY[i] > 480:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        # enemy limit
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_MX
            enemyY[i] += enemyY_change[i]
        if enemyX[i] > 630:
            enemyX_change[i] = -enemy_MX
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_S = "ready"
            enemy_destroy = mixer.Sound(DIR_SOUND+'expl.wav')
            enemy_destroy.play()
            enemyX[i] = respawn_coor_x()
            enemyY[i] = respawn_coor_y(i * 50)
        enemy(enemyX[i], enemyY[i], i)

    # check if previous bullet is out of screen/hit
    if bulletY <= 0:
        bulletY = 480
        bullet_S = "ready"
    # bullet movement
    if bullet_S == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_PY

    if ((pygame.time.get_ticks() - starting_time_for_fire) / 100) > time_interval_between_fires:
        starting_time_for_fire = pygame.time.get_ticks()
        for i in range(number_of_fires):
            # which enemy will fire
            which_enemy_fire = random.randint(0, 4)
            if fire_state[which_enemy_fire] == "ready" and enemyY[which_enemy_fire] > 0:
                fireX[which_enemy_fire] = enemyX[which_enemy_fire]
                fireY[which_enemy_fire] = enemyY[which_enemy_fire]
                fire_by_enemy(fireX[which_enemy_fire], fireY[which_enemy_fire])
                fire_state[which_enemy_fire] = "fire"

    for i in range(number_of_enemies):
        if fire_state[i] == "fire" and enemyY[i] > 0:
            fire_by_enemy(fireX[i], fireY[i])
            fireY[i] += 1
            hit_player = isCollision(playerX, playerY, fireX[i], fireY[i])
            if hit_player:
                fireY[i] = 2000
                player_killed = mixer.Sound(DIR_SOUND+"expl.wav")
                player_killed.play()
                for j in range(number_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break
        if fireY[i] > 600:
            fire_state[i] = "ready"

    player(playerX, playerY)
    pygame.display.update()
