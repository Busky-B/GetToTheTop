import random
from turtle import width
import pygame, sys, time
from pygame.locals import *

# local files
from background import Background
from player import Player
pygame.init()

WINHEIGHT = 1024
WINWIDTH = 600

# main window surface
winSur = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0 , 32)
pygame.display.set_caption('Get to the top!')

BG_IMG_PATH = "assets/bg_img.png"
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
PLAYERONPLATFORM = False
GAMESPEED = 2
RANDOMIZEMAP = True
DEBUG = True
REVERSED = False
PLAYER_WON = False
PLAYER_POINTS = 0
idle_img_counter = 0

'''
    Scales the @param surf object to a set size
    -----
    Used by player_sprite_direction_handler()
'''
def scale_sprite(surface, width, height):
    # return pygame.transform.scale(surface(width, height))
    pass
def scale_player_sprite(surf):
    return pygame.transform.scale(surf, (50, 60))

'''
    Array for storing the IDLE sprites for player character
'''
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
idle_img_left = "assets/MascotBunnyCharacter/Bunny1/01-Idle/__Bunny1_Idle_000.png"
idle_img_left_loaded = scale_player_sprite(pygame.image.load(idle_img_left))
idle_img_right = "assets/MascotBunnyCharacter/Bunny1/01-Idle/__Bunny1_Idle_000_REVERSE.png"
idle_img_right_loaded = scale_player_sprite(pygame.image.load(idle_img_right))
jump_img_left = "assets/MascotBunnyCharacter/Bunny1/06-Jump&Fall/__Bunny1_Fall_000.png"
jump_img_left_loaded = scale_player_sprite(pygame.image.load(jump_img_left))
jump_img_right = "assets/MascotBunnyCharacter/Bunny1/06-Jump&Fall/__Bunny1_Fall_000_REVERSED.png"
jump_img_right_loaded = scale_player_sprite(pygame.image.load(jump_img_right))
grounded = GROUNDED

'''
    Platform  assets path's
'''
platform_path = "assets/platforms/mk1.png"

'''
    Predefined touples with colorcodes (RGB)
'''
WHITE = (255, 255, 255)
BLACK =(0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
bg = Background(BG_IMG_PATH, [0,0])

'''
    Creation of inital 3 platforms
    -----
    When sprites for platforms are implemented this system becomes obsolete,
        we can then just create a rect and skip the Dict with color key
'''
test_obst = pygame.image.load(platform_path)
test_rect = test_obst.get_rect()
test_rect.top = 0
test_rect.left = 5

obst1 = {'rect': pygame.Rect(10, WINHEIGHT - 150, 100, 50), 'color': RED, 'img': test_obst, 'jumped_on' : False}
obst2 = {'rect': pygame.Rect(300, WINHEIGHT - 300, 100, 50), 'color': RED, 'img': test_obst, 'jumped_on' : False}
obst3 = {'rect': pygame.Rect(25, WINHEIGHT - 450, 100, 50), 'color': RED, 'img': test_obst, 'jumped_on' : False}
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
    previous_obstacle = 2 # since 0, 1 ,2 is hardcoded
    platform_height = WINHEIGHT - 600
    while count < 100:
        #stor och liten
        # width_of_platform = random.randint(10,250)
        width_of_platform = 100
        obstacles.append({'rect': pygame.Rect(random.randint(10, WINWIDTH - 50), platform_height, width_of_platform, 50), 'color': RED, 'img': pygame.transform.scale(pygame.image.load(platform_path), (width_of_platform, 50)), 'jumped_on' : False})
        # obstacles.append({'rect': pygame.Rect(random.randint(10, WINWIDTH - 50), platform_height, 100, 50), 'color': RED, 'img': pygame.image.load(platform_path)})
        count += 1
        platform_height -= 125

def randomize_obstacle_xaxis(obst):
    x = obst['rect'].left
    # direction 

'''
    Handle which sprite to use based on playermovement
    ---
    in order to not tax the system (god im just talking out of my ass), a global var is used for not spamming the function
'''
def player_sprite_direction_handler():
    # TODO: remake this so it doesn't use a global varible
    global idle_img_counter 

    if GROUNDED: # player IDLE
        if not REVERSED:
            new_img = idle_img_left_loaded
            idle_img_counter +=1
        else:
            new_img = idle_img_right_loaded

    else: # player FALLING/JUMPING
        if not REVERSED:
            new_img = jump_img_left_loaded
        else:
            new_img = jump_img_right_loaded

    return new_img

# GameLoop
def game_loop():
    global REVERSED
    global JUMPING
    global FALLING
    global ACCEL
    global GROUNDED
    global PLAYER_WON
    
    Game = True
    while Game:
        player_surface = player_sprite_direction_handler() # Handler for direction of sprite

        '''
            Check win / loose condition
            --
            Causes the game to end
        '''
        if player.top <= 0:
            PLAYER_WON = True
            Game = False
        elif player.bottom == WINHEIGHT:
            Game = False

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
            Handle horizontal movement input from keyboard
        '''
        key_state = pygame.key.get_pressed() # get keyboardstate
        player.left +=  (key_state[pygame.K_RIGHT] * MOVESPEED) - (key_state[pygame.K_LEFT] * MOVESPEED)
        player.left +=  (key_state[pygame.K_k] * MOVESPEED) - (key_state[pygame.K_j] * MOVESPEED)
        
        '''
            Handle reversed state of sprite when player moves right or left
        '''
        if key_state[pygame.K_k] or key_state[pygame.K_RIGHT] and not REVERSED:
            REVERSED = True
        if key_state[pygame.K_j] or key_state[pygame.K_LEFT] and REVERSED:
            REVERSED = False

        # Should change this to (if not GROUNDED:)
        if JUMPING or FALLING:
            # GRAVITY
            GRAVITY = 10
            player.top += GRAVITY * ACCEL
            ACCEL += 0.1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # HANDLE JUMPING INPUT
                if GROUNDED: # Prevent "air"jumps
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

        # Draw Background
        winSur.blit(pygame.transform.scale(bg.image, (WINWIDTH, WINHEIGHT)), bg.rect)

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
                        if not obstacle['jumped_on']:
                            add_player_points(1)
                            obstacle['jumped_on'] = True
                
                elif player.bottom > obstacle['rect'].centery:
                    # player touched bottom side, send back to ground
                    GRAVITY = 10
                    ACCEL = 0.1
        if not player.colliderect(ACTIVEPLATFORM) and player.bottom != WINHEIGHT and not JUMPING and not FALLING:
            # make player fall
            FALLING = True
            GROUNDED = False

        '''
            Check if player goes out of bounds
            -----
            if so, put them back in on left or right side respectively
        '''
        if player.left < 0:
            player.left = 0
        if player.right > WINWIDTH:
            player.left = WINWIDTH - player.width

        '''
            Draw the platforms
        '''
        for obst in obstacles: 
            winSur.blit(obst['img'], obst['rect'])
        
        # Draw player
        winSur.blit(player_surface, player)
        create_point_label()# shows textlabel for player points

        pygame.display.update()

        time.sleep(0.01)
        # time.sleep(0.018) # Required in order to not make the game move too fast 
def menu_screen(msg = 'Press any key to start the game . . .', txt_bg_color = BLACK, t_sleep = 0):
    font = pygame.font.SysFont(None, 48)
    startscreen_text = font.render(msg, True, (255,255,255), txt_bg_color)
    startscreen_rect = startscreen_text.get_rect()
    startscreen_rect.centerx = winSur.get_rect().centerx
    startscreen_rect.centery = winSur.get_rect().centery

    global bg

    start_game = False
    while not start_game:
        # winSur.fill((0,255,0))                
        winSur.blit(pygame.transform.scale(bg.image, (WINWIDTH, WINHEIGHT)), bg.rect)
        winSur.blit(startscreen_text, startscreen_rect)
        for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        # HANDLE MOVEMENT INPUT
                        start_game = True
                            
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
        pygame.display.update()
        time.sleep(0.1)
    time.sleep(t_sleep)

def add_player_points(n):
    global PLAYER_POINTS
    PLAYER_POINTS += n

def create_point_label():
    global PLAYER_POINTS

    font = pygame.font.SysFont(None, 48)
    points_surface  = font.render(f'Points: {PLAYER_POINTS}', True, (255,255,255), (0, 0, 0))
    points_rect = points_surface.get_rect()

    winSur.blit(points_surface, points_rect)

if __name__ == "__main__":
    menu_screen()
    game_loop()
    if PLAYER_WON:
        menu_screen("You are a Winner!", GREEN, 2)
    else:
        menu_screen("Game Over!", RED, 3)