#space invader (ship and bullets)
import math
import pygame
import random
from pygame import mixer

#initializing pygame
pygame.init()

#change number of enemies
num_of_enemies = 50
#change player speed
step = 1.9

# score 
score_value = 0
font = pygame.font.Font("assets//Sportive-Regular.ttf", 32)
font2 = pygame.font.Font("assets//font2.otf", 100)

#font size
TextX = 10
TextY = 10

#creating game window
screen_w = 800
screen_h = 600
screen = pygame.display.set_mode((screen_w,screen_h))

#change title
pygame.display.set_caption("Space Invaders")

#change icon
icon = pygame.image.load("assets//icon.png") #define icon
pygame.display.set_icon(icon)             #set the icon


#rocket icon from Flaticon by Freepik
#add player
PlayerImg = pygame.image.load("assets//rocket.png") #define player

#Load background image
bg = pygame.image.load("assets//bck.jpg")
#Load background music
mixer.music.load("assets//bck_music.mp3")
mixer.music.play(-1)

PlayerX = 370
PlayerY = 480
dead_or_alive = "alive"

#Load bullet image
bulletIMG = pygame.image.load("assets//bullet_24.png")

Bullet_X = PlayerX
Bullet_Y = PlayerY + 15
Bullet_speed = 0.5
bullet_state = "ready"
bullet_sound = mixer.Sound("assets//laser1.wav")
death_sound = mixer.Sound("assets//die.wav")

#ready means bullet is invisible
#fire means bullets are firing

enemy1 = pygame.image.load("assets//enemy1.png") #import enemy image
enemy2 = pygame.image.load("assets//enemy2.png") #import enemy image
enemy3 = pygame.image.load("assets//enemy3.png") #import enemy image

enemyimgs = [enemy1,enemy2,enemy3]
enemyIMG = []
enemy_states = []
enemy_X = []
enemy_Y =[]
enemy_X_change = []
enemy_Y_change = []

for i in range(num_of_enemies):
    enemyIMG.append(random.choice(enemyimgs))
    enemy_states.append("show")
    enemy_X.append(random.randint(40,screen_w))
    enemy_Y.append(random.randint(40,150))
    enemy_X_change.append(0.7)
    enemy_Y_change.append(random.randint(14,24))
stepX = 0
stepY = 0


def game_over(x,y):
    screen.fill((255,255,255,0.5)) #change background color - RGB
    game_o = font2.render("GAME OVER",True, (0, 0, 0))
    screen.blit(game_o, (x, y))

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True, (255, 255, 255))
    screen.blit(score, (x, y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x+32, y+10))
    screen.blit(bulletIMG, (x-16, y+10))

def player(x,y):
    screen.blit(PlayerImg,(x,y))

def enemy(Img, x,y):
    screen.blit(Img,(x,y))

def isCollision(x_e, y_e, x_b, y_b):
    distance = math.sqrt(math.pow(x_e-x_b,2) + math.pow(y_e-y_b,2))
    if distance < 20:
        return True
    else:
        return False
#closing window - add quit event
running = True

while running:
    
    #screen.fill((255,155,10)) #change background color - RGB
    #INSIDE OF THE GAME LOOP
    screen.blit(bg, (0, 0))
    
    for event in pygame.event.get():      #get all user events
        try:
            if event.type == pygame.QUIT:     # pressing the close button = Pygame.Quit
                running = False               #quit the window
                pygame.display.quit()
                pygame.quit()
                break
            #get keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    stepY = -step 
                if event.key == pygame.K_DOWN:
                    stepY = step
                if event.key == pygame.K_RIGHT:
                    stepX = step
                if event.key == pygame.K_LEFT:
                    stepX = -step
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        fire_bullet(Bullet_X, Bullet_Y)
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    stepY = 0
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                    stepX = 0
                if (event.key == pygame.K_SPACE):
                    bullet_state = "ready"
                    
        except Exception as e:
            print(e)
        
    #anything that you want to stay inside thescreen need to be inside the while loop
 
    try:
        PlayerX += stepX   
        PlayerY += stepY
        
        #keep the spaceship inside the screen
        if (PlayerX <= 0):             #left side
            PlayerX = 0
        elif (PlayerX >= screen_w-70): #right side
            PlayerX = screen_w-70 
            
        if (PlayerY >= screen_h-70):   #bottom side
            PlayerY = screen_h-70
            
        if (PlayerY <= 10):            #up side
            PlayerY = 10
            
        #show player
        if dead_or_alive == "alive":
            player(PlayerX,PlayerY) #call it after fill because order matters
        else:
            game_over((screen_w/2)-120, (screen_h/2)-40)
        
        #collision
        for i in range(num_of_enemies):   
            enemy_X[i] += enemy_X_change[i]
            if enemy_X[i] >= screen_w-70 or enemy_X[i] <= 30 :
                enemy_X_change[i] = -enemy_X_change[i]
                enemy_Y[i] += 20
                
            if enemy_states[i] == 'show':
                enemy(enemyIMG[i], enemy_X[i],enemy_Y[i])
            collision = isCollision(enemy_X[i], enemy_Y[i], Bullet_X, Bullet_Y)
            if collision:
                death_sound.play()
                Bullet_Y = PlayerY
                Bullet_X = PlayerX
                #bullet_state = "ready"
                enemy_states[i] = 'hide'
                enemy_Y[i] = 0
                enemy_X[i] = 0
                score_value += 400
            collision_p = isCollision(enemy_X[i], enemy_Y[i], PlayerX, PlayerY)
            if collision_p:
                death_sound.play()
                dead_or_alive = "dead"
                PlayerX = 370
                PlayerY = 480               
                for j in range(num_of_enemies):   
                    enemy_states[j] = 'hide'              
        #making bullet ready for firing again
        if Bullet_Y <= 0:
            Bullet_Y = PlayerY + 15
            bullet_state == "ready"
            Bullet_X = PlayerX
        #bullet movement
        if bullet_state == "fire" :
            bullet_sound.play()
            fire_bullet(Bullet_X,Bullet_Y)
            Bullet_Y -= 40

    
        #show scare
        show_score(TextX, TextY)
        pygame.display.update()   #to update screen
    except Exception as e:
        print(e)
