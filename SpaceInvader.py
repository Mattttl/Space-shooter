import math
import random
import pygame

s_width = 800
s_height = 500
player_startx = 370
player_starty = 380
enemy_start_y_min = -150
enemy_start_y_max = -100
enemy_speedx= 0.5
enemy_speedy = 40
e_width = 50
e_height = e_width

bullet_speedy = 10
collision_distance = 27
player_speed = 1
background = pygame.image.load('darkPurple.png')
background = pygame.transform.scale(background,(s_width,s_height))

pygame.init()
screen = pygame.display.set_mode((s_width, s_height))

pygame.display.set_caption('Space Invader')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = player_startx
playery = player_starty
player_speedx = 0

enemyImg = []

enemyX = []
enemyY = []
enemyX_speed = []
enemyY_speed = []
enemies = 6
for i in range(enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,s_width-64))
    enemyY.append(random.randint(enemy_start_y_min,enemy_start_y_max))
    enemyX_speed.append(enemy_speedx)
    enemyY_speed.append(enemy_speedy)
    enemyImg[i] = pygame.transform.scale(enemyImg[i],(e_width,e_height))
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = player_starty
bulletx_speed = 0
bullety_speed = bullet_speedy
bullet_state = 'ready'

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX= 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score= font.render('Score : '+ str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))
def over_score():
    over_text= over_font.render('GAME OVER',True, (255,255,255))
    screen.blit(over_text,(200,250))
def player(x,y):
    screen.blit(playerImg,(x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state= 'fire'
    screen.blit(bulletImg, (x+16, y+10))
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))
def isCollision(enemyX,enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY)**2)
    return distance < collision_distance

pygame.display.update()

running = True

while running:
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_speedx = -player_speed
            if event.key == pygame.K_d:
                player_speedx = player_speed
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP and event.key in [pygame.K_d,pygame.K_a]:
            player_speedx = 0
    playerX += player_speedx
    playerX = max(0,min(playerX,s_width - 64))
    for i in range(enemies):
        if enemyY[i] > 340:
            for j in range(enemies):
                enemyY[j]= 2000
            over_score()
            break
        enemyX[i] += enemyX_speed[i]
        if enemyX[i] <= 0 or enemyX[i] >= s_width - 64:
            enemyX_speed[i] *= -1
            enemyY[i] += enemyY_speed[i]
        if isCollision(enemyX[i],enemyY[i],bulletX,bulletY):
            bulletY = player_starty
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,s_width - 64)
            enemyY[i] = random.randint(enemy_start_y_min,enemy_start_y_max)
        enemy(enemyX[i],enemyY[i],i)
    if bulletY <=0:
        bulletY=player_starty
        bullet_state = 'ready'
    elif bullet_state == 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bullet_speedy
    player(playerX,playery)
    show_score(textX,textY)
    pygame.display.update()
pygame.quit()