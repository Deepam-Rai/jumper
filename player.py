# A module to handle all the stats and aspects of player object

import pygame,sys

#we also use static variables of platform module
from platform import Platform

#pre-initializing mixer to avoid the jumpsound delay
pygame.mixer.pre_init( 44100, -16, 2, 512)

class Player:
    '''The class tht handles everything of the player'''
    def __init__(self, game):
        '''Here we initialize the data of the player'''
        super().__init__()

        #holds the main game data
        self.main_game = game
        #the screen of the main game
        self.game_screen = game.screen

        #initialize the player's data
        self.init_player()

        #animation and collision data
        self.animation_db = []
        self.current_frame=0
        #a function which loads the sprites from given path
        self.load_animation('./sprites/Player/Rogue/high_jump', [10,10,10,10,10,10,10,10,10,10,10,10])
        self.image = self.animation_db[0]
        self.rect = self.image.get_rect()   #for player collision check

        #player stats data
        self.life = 3
        self.score = 0
        self.life_icon = pygame.image.load("./sprites/Player/Rogue/Life/life.png")


        #sounds and music
        self.jump_sound = pygame.mixer.Sound("./Sound/jump.wav")
    
    def init_player(self):
        '''Initializes the player's position'''
        #movement data
        self.moving_right = False
        self.moving_left = False
        #setting the initial position of the player
        self.location = {'x': self.main_game.WINDOW_SIZE[0]/2,'y':0}
        self.y_momentum = 0
        self.flip = False  #is true when the player is facing left

    def update(self):
        '''Moves the player as per the movement data'''
        #updating the player's location
        if self.moving_right == True:
            self.location['x']+=4
        if self.moving_left == True:
            self.location['x']-=4
        
        #increase y-momentum; player comes down
        self.y_momentum +=0.3
        #add momentum to the downward movement
        self.location['y'] += self.y_momentum
        
        #check if player passed side edges of the screen; if yes then warp to the another side
        if self.location['x'] > self.main_game.WINDOW_SIZE[0]:
            self.location['x'] = 0
        elif self.location['x'] + self.image.get_width()< 0 :
            self.location['x'] = self.main_game.WINDOW_SIZE[0] - self.image.get_width()

        #updating the player's rect  for collision detection
        self.rect.x = self.location['x']
        self.rect.y = self.location['y']
    
    def collision_check(self):
        '''checks the collision with all platforms and screen edges'''
        for platform in self.main_game.platform_db:
            #check with each and every platform
            if self.rect.colliderect( platform.rect):
                #if collision has occured

                if self.y_momentum>0 and self.location['y'] + self.image.get_height()/2 < platform.location['y']:
                # check if collision was because of jumping upon platform
                    #then only that collision is valid
                    #check if it is a fatal collision
                    if platform.platform_type == Platform.FATAL:
                        #decrease the player's life
                        print("Be careful next time!")
                        self.life -=1
                    platform.location['y'] +=10 #push the platform little down
                    self.y_momentum *= -1       #player's movement direction is reversed
                    self.jump_sound.play()      #player jumps on the platform
                    #restart the jumping animation
                    self.current_frame = 0
                    #increase the player's score
                    self.score += platform.points
        #check if player has reached the bottom of the screen then decrease life
        if self.location['y'] > self.main_game.WINDOW_SIZE[1]:
            print("You Reached the Abyss.")
            self.life -=1
            #return the player to initial position
            self.init_player()
        
    def display_stats(self):
        '''Displays the player's stats into the screen'''
        #1. create the font
        font = pygame.font.Font('freesansbold.ttf', 32)
        #2. create the text surface object
        stats = font.render(str(self.score), False, (0,0,0))
        #3. blit it
        self.game_screen.blit( stats, [10,10])

        #display life
        for i in range(self.life):
            self.game_screen.blit(self.life_icon, [ i*20, 50])

    def blitIt(self):
        '''Blits the player into the screen'''
        self.current_frame +=1
        #if end of frames for animation is reached, then reset current animation frame to 0
        if( self.current_frame >= len(self.animation_db)):
            self.current_frame = 0
        #pick up the image for current frame
        self.image = self.animation_db[self.current_frame]
        #if we are moving left then we also flip the character image image
        self.game_screen.blit( pygame.transform.flip(self.image, self.flip, False), self.rect)

    def load_animation(self, path, frame_duration_arr):
        '''loads the png images and makes it ready for blitting'''
        animation_name = path.split('/')[-1]    #getting the prefix names of images which is same as folder name
        n=0 #to keep track of the number of images
        for frame in frame_duration_arr:
            #an iteration for each image; frame contains the count of frames that this image should persist for
            image_path = path + '/' + animation_name + str(n+1) + ".png"
            #loading the image
            image = pygame.image.load( image_path)
            #image.set_colorkey((255,255,255)) #to make white color transparent; not needed in these png
            for i in range(frame):
                #put these image(duplicates) frame many number of times in animation
                self.animation_db.append(image.copy())
            n+=1    #move to next image
        return

