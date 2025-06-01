import pgzrun
import random
import math
from pygame import Rect  # unico modulo permitido do pygame


WIDTH = 1000
HEIGHT = 600

#Ativar o som
SOUND_ON = True

#Carregar o som ou música
music.set_volume(0) #volume da música
music.play('background_music') #música 

floor = Rect((0, 580),(1000, 20))
groundcolour = 80,70,55
groundcolour_x = 21,24,38,255


#heroi
hero = Actor('player.gif', (500, 250))
hero_x_velocity = 0
hero_y_velocity = 0
gravity = 1
jumping = False
jumped = False
lives = 3


#plataformas

platform1 = Rect((450, 500), (100,10))
platform2 = Rect((300, 400), (100,10))
platform3 = Rect((600, 400), (100,10))
platform4 = Rect((200, 300), (100,10))
platform5 = Rect((700, 300), (100,10))
platform6 = Rect((100, 200), (100,10))
platform7 = Rect((800, 200), (100,10))
platform8 = Rect((10, 100), (100,10))
platform9 = Rect((890, 100), (100,10))
platform10 = Rect((100, 400), (100,10))
platform11 = Rect((800, 400), (100,10))
platform12 = Rect((450, 300), (100,10))

platforms = [floor,platform1,platform2,platform3,platform4,platform5,platform6,platform7,platform8,platform9,platform10,platform11,platform12]

#moedas

coin_x = [950,50,850,150,750,250,650,350,500]
coin_y = [70,70,170,170,270,270,370,370,470]
c_xy = random.randint(0,8)
coin = Actor('coin_1.gif', (coin_x[c_xy], coin_y[c_xy]))
points = 0

#monstro voador
eyes_monster_images = ['eyes_monster1','eyes_monster2','eyes_monster3','eyes_monster4','eyes_monster5','eyes_monster6','eyes_monster7']
eyes_monster = Actor(eyes_monster_images[0], (0,100))
eyes_monster.speed = 3
eyes_monster.direction = 1
eyes_monster.frame = 0
eyes_monster.animation_speed = 0.2

#monstro terrestre
dragon_images = ['dragon1','dragon1.1','dragon2','dragon3','dragon4','dragon5','dragon6','dragon7','dragon8']
dragon = Actor(dragon_images[0], (0,550))
dragon.speed = 1.5
dragon.direction = 1
dragon.frame = 0
dragon.animation_speed = 0.1
dragon.is_alive = True

#versao onde as plataformas ficam dinamicas>

def update():
    hero_move()
    update_eyes_monster()
    update_dragon()

    if hero.colliderect(eyes_monster) or hero.colliderect(dragon):
        sounds.death.play()
        reset_hero_position()

def update_eyes_monster():

    eyes_monster.frame += eyes_monster.animation_speed
    if eyes_monster.frame >= len(eyes_monster_images):
        eyes_monster.frame = 0
    eyes_monster.image = eyes_monster_images[int(eyes_monster.frame)]

    eyes_monster.x += eyes_monster.speed * eyes_monster.direction

    if eyes_monster.x > WIDTH:
        eyes_monster.direction =-1
        eyes_monster.y += 20
    elif eyes_monster.x < 0:
        eyes_monster.direction = 1
    if eyes_monster.y <50:
        eyes_monster.y = 50
    elif eyes_monster.y >150:
        eyes_monster.y =100

def reset_hero_position():
    global points, lives
    hero.x = 500
    hero.y = 250
    points = max(0, points - 1)
    lives -= 1
    if lives <= 0:
        points = 0
        lives = 3 


def update_dragon():
    if not dragon.is_alive:
        return
    dragon.frame += dragon.animation_speed
    if dragon.frame >= len(dragon_images):
        dragon.frame = 0
    dragon.image = dragon_images[int(dragon.frame)]

    dragon.x += dragon.speed * dragon.direction

    if dragon.direction == -1:
        dragon.flip_x = True
    else:
        dragon.flip_x = False
    
    if dragon.right > WIDTH:
        dragon.direction = -1
    elif dragon.left < 0:
        dragon.direction = 1
    
    dragon.y =550

def hero_move():
    global hero_x_velocity, hero_y_velocity, jumping, gravity, jumped, points, c_xy

    if hero_x_velocity == 0 and not jumped:
        hero.image = 'player'
    
    if collidecheck():
        gravity = 1
        hero.y -=1
    if not collidecheck():
        hero.y += gravity
        if gravity <= 20:
            gravity += 0.5

    if (keyboard.left):
        if (hero.x > 40) and (hero_x_velocity > -8):
            hero_x_velocity -= 2
            hero.image = 'jumper-left'
    if (keyboard.right):
        if (hero.x < 960) and (hero_x_velocity < 8):
            hero_x_velocity += 2
            hero.image = 'jumper-right'

    hero.x += hero_x_velocity

    #velocidade
    if hero_x_velocity > 0:
        hero_x_velocity -=1
    if hero_x_velocity < 0:
        hero_x_velocity +=1 
    if hero.x < 50 or hero.x >950:
        hero_x_velocity = 0

    #pulando
    if (keyboard.up) and collidecheck() and not jumped:
        sounds.jump.play()
        jumping = True
        jumped = True
        clock.schedule_unique(jumpedrecently, 0.4)
        hero.image = 'jump'
        hero_y_velocity = 95
    if jumping and hero_y_velocity > 25:
        hero_y_velocity = hero_y_velocity - ((100 - hero_y_velocity)/2)
        hero.y -= hero_y_velocity/3 
    else: 
        hero_y_velocity = 0
        jumping = False
    
    #pegar moedas

    if hero.colliderect(coin):
        sounds.coin.play()
        points += 1 
        old_c_xy = c_xy
        c_xy = random.randint(0,8)
        while old_c_xy == c_xy:
            c_xy = random.randint(0,8)
        c_xy = random.randint(0,8)
        coin.x = coin_x[c_xy]
        coin.y = coin_y[c_xy]

def draw():
    screen.fill((173, 216, 255))
    screen.blit('floresta', (0,00))
    for i in platforms:
        screen.draw.filled_rect(i, groundcolour)
    screen.draw.filled_rect(floor, groundcolour_x)
    hero.draw()
    coin.draw()
    eyes_monster.draw()
    dragon.draw()
    screen.draw.text("Pontos:", center=(60,30), fontsize=30, shadow=(1,1), color=(255,255,255), scolor='#202020')
    screen.draw.text(str(points), center=(110,30), fontsize=30, shadow=(1,1), color=(255,255,255), scolor='#202020')
    screen.draw.text("Vidas:", center=(200,30), fontsize=30, shadow=(1,1), color=(255,255,255), scolor='#202020')
    screen.draw.text(str(lives), center=(250,30), fontsize=30, shadow=(1,1), color=(255,255,255), scolor='#202020')


def collidecheck():
    collide = False

    for i in platforms:
        if hero.colliderect(i):
            collide = True
    return collide

def jumpedrecently():
    global jumped
    jumped = False