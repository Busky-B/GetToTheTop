import random
import pygame, sys, time
from pygame.locals import *

pygame.init()

WINHEIGHT = 1024
WINWIDTH = 600

# main window surface
winSur = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0 , 32)
pygame.display.set_caption('Boxes - Platformer')

# Vars for Direction
DOWNLEFT = 'downleft'
DOWNRIGHT = 'downright'
UPLEFT = 'upleft'
UPRIGHT = 'upright'
STOP = 'stop'
MOVESPEED = 10
GRAVITY = 4
ACCEL = 1
GROUNDED = False
JUMPING = False
FALLING = True
ACTIVEPLATFORM = pygame.Rect((0,0,0,0))
PLAYERONPLATFORM = False
GAMESPEED = 2
RANDOMIZEMAP = True

#COLOR
WHITE = (255, 255, 255)
BLACK =(0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Boxes structure declaration
box1 = {'rect': pygame.Rect(10, WINHEIGHT - 200, 50, 60), 'color': WHITE, 'dir': UPRIGHT, 'speed': 4}
#box2 = {'rect': pygame.Rect(300, 80, 50, 60), 'color': RED, 'dir': UPLEFT, 'speed': 2}
#box3 = {'rect': pygame.Rect(300, 80, 50, 60), 'color': BLUE, 'dir': DOWNRIGHT, 'speed': 8}
obst1 = {'rect': pygame.Rect(10, WINHEIGHT - 150, 100, 50), 'color': RED}
obst2 = {'rect': pygame.Rect(300, WINHEIGHT - 300, 100, 50), 'color': RED}
obst3 = {'rect': pygame.Rect(25, WINHEIGHT - 450, 100, 50), 'color': RED}

placeholder = [obst1, obst2, obst3]
obstacles = [obst1, obst2, obst3]
b = box1
player = b['rect']

if RANDOMIZEMAP:
    # Randomize map
    count = 0
    platform_height = WINHEIGHT - 600
    while count < 100:
        obstacles.append({'rect': pygame.Rect(random.randint(10, WINWIDTH - 50), platform_height, 100, 50), 'color': RED})
        count += 1
        platform_height -= 125


# GameLoop
while True:
    if player.top == 0:
        print('WINNER')
        pygame.quit()
        sys.exit()

    elif player.bottom == WINHEIGHT:
        print('GAME OVER!')
        pygame.quit()
        sys.exit()
    for obstacle in obstacles:
        if obstacle['rect'].bottom == WINHEIGHT:
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle['rect'].bottom +=1 
    player.bottom += 1
    # for obst in obstacles['rect']:
    #     obst.bottom += GAMESPEED
    # Returns all keys, either true or false. Not good for performance, needed for continous movement
    # print(pygame.key.get_pressed())
    key_state = pygame.key.get_pressed() # get keyboardstate
    b['rect'].left +=  (key_state[pygame.K_RIGHT] * MOVESPEED) - (key_state[pygame.K_LEFT] * MOVESPEED)
    b['rect'].left +=  (key_state[pygame.K_k] * MOVESPEED) - (key_state[pygame.K_j] * MOVESPEED)

    # Should change this to (if not GROUNDED:)
    if JUMPING or FALLING:
        # GRAVITY
        GRAVITY = 10
        b['rect'].top += GRAVITY * ACCEL
        ACCEL += 0.1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # HANDLE MOVEMENT INPUT
            if GROUNDED:#for testing with double jumps or True:
                FALLING = False
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    #b['rect'].top -= 100
                    JUMPING = True
                    GROUNDED = False
                    GRAVITY = 10 
                    player.bottom -= 1 # moves player as to not trigger rect
                    ACCEL = -2
                
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    winSur.fill(BLACK)
    # check if player on ground
    if b['rect'].bottom > WINHEIGHT:
        ACCEL = 1
        GRAVITY = 0
        b['rect'].top = WINHEIGHT - b['rect'].height
        GROUNDED = True
        FALLING = False
        JUMPING = False
    # check if player is on platform
    
    for obstacle in obstacles:
        obs = obstacle['rect']
        if player.colliderect(obstacle['rect']):
            if player.bottom <= obstacle['rect'].centery:
                if not GROUNDED:
                    print('inside ontop')
                    ACTIVEPLATFORM = obstacle['rect'] 
                    GRAVITY = 0
                    player.bottom = obstacle['rect'].top + 1# + for down
                    JUMPING = False
                    FALLING = False
                    GROUNDED = True 
            
            elif b['rect'].bottom > obstacle['rect'].centery:
                print('inside bottom')
                # player touched bottom side, send back to ground
                GRAVITY = 10
                ACCEL = 0.1
    if not player.colliderect(ACTIVEPLATFORM) and b['rect'].bottom != WINHEIGHT and not JUMPING and not FALLING:
        print('inside out of platform')
        # make player fall
        FALLING = True
        GROUNDED = False

            


    # The box has moved past the left side.
    if b['rect'].left < 0:
        b['rect'].left = 0
    # The box has moved past the right side.
    if b['rect'].right > WINWIDTH:
        b['rect'].left = WINWIDTH - b['rect'].width

        
    pygame.draw.rect(winSur, b['color'], b['rect'])
    
    for obst in obstacles: # Draw platforms
        pygame.draw.rect(winSur, obst['color'], obst['rect'])

    pygame.display.update()

    time.sleep(0.02)
            
def horizontal_movement(b):
    pass
    
def fall_down():
    pass