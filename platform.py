# This is a self-made module for the platforms or pads in the game
#player can jump on this platform in order to not fall down

import pygame

class Platform:
    '''This class represents a single platform upon which player can jump in the game.
    In the game we use a list of such platforms.'''
    #class variables; shared by all of the instances and accessible even without any instance.
    #movement data; since all platforms move at the same base speed
    base_y_momentum = 3 #tells by how much he platform moves down the screen

    #platform types
    PLAIN = "Pad_02_1"  #class constants for different kinds of platforms
    FATAL = "Pad_02_2"

    def __init__(self, x,y, platform_type, game):
        '''This function initializes the data of a platform after it is created'''
        self.location = { 'x':x, 'y':y}     #setting the location
        self.platform_type = platform_type  #setting the platform type

        #main game data
        self.main_game = game
        self.game_screen = game.screen  #is needed in order to blit this platform onto the screen
        
        #load platform image image
        self.image = pygame.image.load("./sprites/Pads/" + self.platform_type + ".png")
        self.rect = self.image.get_rect()   #required for collision detection

        #stats to give to player
        self.points = 10    #when player jumps on the platform then he is granted 10 points

    def update(self):
        #function to update the platform location
        self.location['y']+= Platform.base_y_momentum
        #update its rect for collision detection
        self.rect.x = self.location['x']
        self.rect.y = self.location['y']

    def blitIt(self):
        '''Display the platform pad into the screen'''
        self.game_screen.blit( self.image, self.rect)
