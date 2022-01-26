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
DEBUG = True
REVERSED = False
idle_img_left_arr = [
    "assets/MascotBunnyCharacter/Bunny1/01-Idle/idle1.png",
    "assets/MascotBunnyCharacter/Bunny1/01-Idle/idle2.png",
    "assets/MascotBunnyCharacter/Bunny1/01-Idle/idle3.png",
    "assets/MascotBunnyCharacter/Bunny1/01-Idle/idle4.png",
    "assets/MascotBunnyCharacter/Bunny1/01-Idle/idle5.png",
    "assets/MascotBunnyCharacter/Bunny1/01-Idle/idle6.png",
    "assets/MascotBunnyCharacter/Bunny1/01-Idle/idle7.png",
    "assets/MascotBunnyCharacter/Bunny1/01-Idle/idle8.png",
    "assets/MascotBunnyCharacter/Bunny1/01-Idle/idle9.png",
]
idle_img_counter = 0
idle_img_left = "assets/MascotBunnyCharacter/Bunny1/01-Idle/__Bunny1_Idle_000.png"
idle_img_right = "assets/MascotBunnyCharacter/Bunny1/01-Idle/__Bunny1_Idle_000_REVERSE.png"
jump_img_left = "assets/MascotBunnyCharacter/Bunny1/06-Jump&Fall/__Bunny1_Fall_000.png"
jump_img_right = "assets/MascotBunnyCharacter/Bunny1/06-Jump&Fall/__Bunny1_Fall_000_REVERSED.png"
grounded = GROUNDED
#COLOR
WHITE = (255, 255, 255)
BLACK =(0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Boxes structure declaration
# box1 = {'rect': pygame.Rect(10, WINHEIGHT - 200, 50, 60), 'color': WHITE, 'dir': UPRIGHT, 'speed': 4}
'''
    Creation of inital 3 platforms
    -----
    When sprites for platforms are implemented this system becomes obsolete,
        we can then just create a rect and skip the Dict with color key
'''
obst1 = {'rect': pygame.Rect(10, WINHEIGHT - 150, 100, 50), 'color': RED}
obst2 = {'rect': pygame.Rect(300, WINHEIGHT - 300, 100, 50), 'color': RED}
obst3 = {'rect': pygame.Rect(25, WINHEIGHT - 450, 100, 50), 'color': RED}
obstacles = [obst1, obst2, obst3]

'''
    Creation of player Surface and Rect
    -----
    Transforming scale due to images being to large
    adds a starting pos for player
'''
player_surface = pygame.transform.scale(pygame.image.load(idle_img_left), (50, 60))
player = player_surface.get_rect() # Creat Rect from the imageSurface
player.top = WINHEIGHT - 200 # put player starting position at first platform

'''
    Expression for inputing randomized map
    -----
    This is meant as a debugging tool and will probably be removed,
    randomization needs a rework since maps can be unbeatable
'''
if RANDOMIZEMAP:
    # Randomize map
    count = 0
    platform_height = WINHEIGHT - 600
    while count < 100:
        obstacles.append({'rect': pygame.Rect(random.randint(10, WINWIDTH - 50), platform_height, 100, 50), 'color': RED})
        count += 1
        platform_height -= 125
'''
    Scales the @param surf object to a set size
    -----
    Used by player_sprite_direction_handler()
'''
def scale_player_sprite(surf):
    return pygame.transform.scale(surf, (50, 60))
'''
    Handle which sprite to use based on playermovement
    ---
    in order to not tax the system (god im just talking out of my ass), a global var is used for not spamming the function
'''
def player_sprite_direction_handler():
    # TODO: remake this so it doesn't use a global varible
    global REVERSED
    global idle_img_counter
    

    if GROUNDED: # player IDLE
        if not REVERSED:
            new_img  = scale_player_sprite(pygame.image.load(idle_img_left_arr[idle_img_counter])) # WORKS NOW
            idle_img_counter +=1
        else:
            new_img = scale_player_sprite(pygame.image.load(idle_img_right))

    else: # player FALLING/JUMPING
        if not REVERSED:
            new_img  = scale_player_sprite(pygame.image.load(jump_img_left))
        else:
            new_img = scale_player_sprite(pygame.image.load(jump_img_right))

    return new_img

# GameLoop
while True:
    # prevent out of range 
    if idle_img_counter +1 >= 8:
        idle_img_counter = 0
    # this needs to be moved into directionhandler func
    player_surface = player_sprite_direction_handler()

    '''
        Check win / loose condition
    '''
    if player.top == 0:
        if not DEBUG:
            print('WINNER')
            pygame.quit()
            sys.exit()
    elif player.bottom == WINHEIGHT:
        if not DEBUG:
            print('GAME OVER!')
            pygame.quit()
            sys.exit()
    '''
        Remove platforms when they reach the bottom
    '''
    for obstacle in obstacles:
        if obstacle['rect'].bottom == WINHEIGHT: # remove if rect hits bottom
            obstacles.pop(obstacles.index(obstacle))
        else: # Else move rect down
            obstacle['rect'].bottom +=1 
    player.bottom += 1 # Player needs to be moved down aswell to stay fixed on top of platform
    '''
        Handle movement input from keyboard
    '''
    key_state = pygame.key.get_pressed() # get keyboardstate
    player.left +=  (key_state[pygame.K_RIGHT] * MOVESPEED) - (key_state[pygame.K_LEFT] * MOVESPEED)
    player.left +=  (key_state[pygame.K_k] * MOVESPEED) - (key_state[pygame.K_j] * MOVESPEED)
    
    '''
        Handle reversed state of sprite when player moves right or left
    '''
    if key_state[pygame.K_k] and not REVERSED:
        REVERSED = True
        # player_surface = change_direction_player_sprite('right')
    if key_state[pygame.K_j] and REVERSED:
        REVERSED = False
        # player_surface = change_direction_player_sprite('left')


    # Should change this to (if not GROUNDED:)
    if JUMPING or FALLING:
        # GRAVITY
        GRAVITY = 10
        player.top += GRAVITY * ACCEL
        ACCEL += 0.1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # HANDLE MOVEMENT INPUT
            if GROUNDED:#for testing with double jumps or True:
                FALLING = False
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
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
    if player.bottom > WINHEIGHT:
        ACCEL = 1
        GRAVITY = 0
        player.top = WINHEIGHT - player.height
        GROUNDED = True
        FALLING = False
        JUMPING = False
    # check if player is on platform
    
    for obstacle in obstacles:
        obs = obstacle['rect']
        if player.colliderect(obstacle['rect']):
            if player.bottom <= obstacle['rect'].centery:
                if not GROUNDED:
                    ACTIVEPLATFORM = obstacle['rect'] 
                    GRAVITY = 0
                    player.bottom = obstacle['rect'].top + 1# + for down
                    JUMPING = False
                    FALLING = False
                    GROUNDED = True 
            
            elif player.bottom > obstacle['rect'].centery:
                # player touched bottom side, send back to ground
                GRAVITY = 10
                ACCEL = 0.1
    if not player.colliderect(ACTIVEPLATFORM) and player.bottom != WINHEIGHT and not JUMPING and not FALLING:
        # make player fall
        FALLING = True
        GROUNDED = False

            


    # The box has moved past the left side.
    if player.left < 0:
        player.left = 0
    # The box has moved past the right side.
    if player.right > WINWIDTH:
        player.left = WINWIDTH - player.width

        
    # pygame.draw.rect(winSur, b['color'], b['rect'])
    
    for obst in obstacles: # Draw platforms
        pygame.draw.rect(winSur, obst['color'], obst['rect'])
    
    # drawing image on rect
    winSur.blit(player_surface, player)
    # pygame.draw.rect(winSur,BLUE, test_rect)


    pygame.display.update()

    time.sleep(0.02)
            
def horizontal_movement(b):
    pass
    
def fall_down():
    pass