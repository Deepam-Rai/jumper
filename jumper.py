# Mini-Project -Jumper
# Built while exploring python pygame module.
# 21231 - Deepam Rai
# I- MSc

import pygame, sys, random  #importing pygame, system and random module
pygame.init()   #initializing the modules of pygame; this is necessary for some modules
pygame.mixer.pre_init( 44100, -16, 2, 1024) #pre-initializing mixer so that there is no delay in sound effects

#importing self made modules for the project
from player import Player
from platform import Platform

class Jumper:
    '''This is the main class which holds everything of our game.
    Whenever and wherever required it imports and uses pygame and other self made modules(player, platform)'''
    def __init__(self):
        '''Here we initialize the values, stats, etc of the game'''

        self.clock = pygame.time.Clock()    #to control the frame rate of the game
        self.menu_font = pygame.font.SysFont('Corbel',35)   #the font that we will use for our menu options

        #setting the title for the display window
        pygame.display.set_caption('Jumper')
        
        self.WINDOW_SIZE = (400,600) #(x,y)#setting the size of the window
        self.FPS = 60   #setting the FPS of the game; this is not floowed strictly

        #setting the main display screen;
        self.screen = pygame.display.set_mode( self.WINDOW_SIZE)
        #loading the background image of the game
        self.bg_image = pygame.image.load("./sprites/Background/bg.png")

        #setting up the platforms data
        self.platform_probability = 0.05    #probability that the platform is created in each line pixel
        self.harmful_platforms = 0.15       #probability that the created platform is harmful to player

        #sounds and music
        pygame.mixer.music.load("./Sound/bg.wav")   #loading the background music
        pygame.mixer.music.play(-1) #setting up the background music to be repeated infinite times

        self.initialize()   #function that initializes stats after every new game

    def initialize(self):
        '''This functino sets the stats for every new game.'''
        self.pause = False          #the game isnt paused initially
        self.player = Player(self)  #a new player object(and hence new stats) is created
        self.platform_db = []       #the platforms are also re-initialized totally
        random.seed()               #This ensures that random module give different vaule on each run


    def run_game(self):
        '''The function responsible for running the game.
            This is where GAME-LOOP is kept'''
        #first creating some linear platforms to help player from fallind down initially
        for i in range(6):
            self.platform_db.append( Platform(random.randint(0, self.WINDOW_SIZE[0]), self.WINDOW_SIZE[1]*2/4, Platform.PLAIN, self))
        #GAME-LOOP
        while self.player.life>0: #game loop        
            if not self.pause:  #if the game is paused then nothing inside the loop is done; menu is displayed
                self.screen.blit( self.bg_image, [0,0]) #displaying the background image on the window
                self.handle_platforms() #this functions creates, destroys, updates platforms as necessary

                #player updates
                self.player.update()            #updates the player's position and stats
                self.player.collision_check()   #player checks if it has collided with anything; and if yes then case is appropriately handled
                self.player.blitIt()            #displaying the player on the screen
                self.player.display_stats()     #displaying the player stats on the screen

                self._check_events()   #checking for the events(inputs- keys, mouse, etc)

                pygame.display.update()#actual updation and hence rendering of all the blittings done on the screen

                self.clock.tick(self.FPS)   #making sure that the game runs at 60fps
        #the loop ends here
        #if execution reaches here then the game is over
        self.pause = True   #to stop the things insie game loop to be executed
        self.menu()         #display the menu


    def _check_events(self):
        ''' To check for user input events -  keyboard inputs, mouse inputs'''
        for event in pygame.event.get():    #iterate throught the event-queue and check of each of them
            if event.type == pygame.QUIT:   #if the event is for quit
                    pygame.quit()   #then quit all pygame modules
                    sys.quit()      #and quit the application from system
            if event.type == pygame.KEYDOWN:    #if the user has pressed down the key
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  #for moving RIGHT
                    self.player.moving_left = False
                    self.player.moving_right = True
                    self.player.flip = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:   #for moving LEFT
                    self.player.moving_right = False
                    self.player.moving_left = True
                    self.player.flip = True #required since our sprite image is right-side facing
            if event.type == pygame.KEYUP:      #when player releases the pressed key
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  #move RIGHT
                    self.player.moving_right = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:   #move LEFT
                    self.player.moving_left = False
                if event.key == pygame.K_s:                                 #PAUSE the game
                    self.pause = True #pause the game
                    self.menu() #and display menu
    
    def menu(self):
        '''Handles the menu of the game. Also handles game over event.'''
        y_coord = 100     #for positioning the buttons
        x_coord = 105
        color_light = (170,170,170)     #color of the buttons
        color_dark = (100,100,100)
        #texts for different buttons
        resume = self.menu_font.render("Resume", False, (255,255,255))
        newgame = self.menu_font.render("New Game", False, (255,255,255))
        go = self.menu_font.render("Game-Over!", False, (255,50,50))
        quit = self.menu_font.render("Quit", False, (255,255,255))
        
        #setting the menu options in a list for ease of use
        #menu options; their coordinate-offsets; their corresponding function references
        options = [  [go, [19,0]], [resume, [43, 4]], [newgame, [24, 4]], [quit, [61, 4]]]
        
        while( self.pause):
            #PART- A: first render all of the buttons
            
            #get the position of the mouse pointer to get mouse hover and clicks
            mouse = pygame.mouse.get_pos()
            
            button = pygame.Rect(x_coord, y_coord, 180, 30) #setting up the rect for the button
            #if the mouse is hovered over then display aligt_color rectangle; else dark color; then blit text upon it
            if self.player.life <1:
                #GAME-OVER  ; this does not need any button
                self.screen.blit(options[0][0], [x_coord+options[0][1][0],y_coord+options[0][1][1]])
            else:
                #RESUME-GAME
                # if mouse is hovered on a button it then changes to lighter shade 
                if button.collidepoint(mouse):
                    pygame.draw.rect(self.screen,color_light,button) 
                else:   #put to darker shade
                    pygame.draw.rect(self.screen,color_dark,button) 
                #putting the text on the button
                self.screen.blit(options[1][0], [x_coord+options[1][1][0],y_coord+options[1][1][1]])
            for i in range(2,4):
                #NEW-GAME & #QUIT buttons
                button.y +=35   #another button is 35 units down
                if button.collidepoint(mouse):                      #if mouse is hovered
                    pygame.draw.rect(self.screen,color_light,button)#then draw a lighter shade button 
                else: 
                    pygame.draw.rect(self.screen,color_dark,button) #else darker shade
                #putting the text on the button
                self.screen.blit(options[i][0], [x_coord+options[i][1][0],y_coord+(i-1)*35+options[i][1][1]])

            #PART-B: check if any button is clicked
            button = pygame.Rect(x_coord, y_coord, 180, 30) #a rect to make checking easier
            for event in pygame.event.get():    #loop through all events in event-queue
                if event.type == pygame.QUIT:   #event to end the program
                    pygame.quit()
                    sys.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:    #mouse was pressed down
                    if self.player.life>0 and button.collidepoint(event.pos):   #on the RESUME button
                        self.pause = False  #just resume the game and return
                        return
                    button.y +=35 #takes to "new game" button
                    if button.collidepoint(event.pos):      #on the NEW-GAME button
                        self.initialize() #initiate stats
                        self.run_game()   #run a totally new game
                        pygame.quit()     #when that game returns. just return; can cause excessive nested calls
                        sys.exit()
                    button.y +=35   #takes to quit button
                    if button.collidepoint(event.pos):      #on the QUIT button
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

    def handle_platforms(self):
        '''The main function to handle the array of platforms.
            The platforms handle themselves at the individual level'''
        
        #create a platform on probability basis
        if( random.random() < self.platform_probability):
            x= random.randint(0, self.WINDOW_SIZE[0])   #x-coordinate of the new platform
            #setting if the new platform is harmful or not to the player
            platform_type = Platform.PLAIN if random.random() > self.harmful_platforms else Platform.FATAL
            #creating and appending the new platform to the existing list of platforms
            self.platform_db.append( Platform(x, 10, platform_type, self))
        
        #update all of the platforms
        for platform in self.platform_db:
            platform.update()
            #remove platforms when they go out of screen
            if platform.location['y']> self.WINDOW_SIZE[1]:
                self.platform_db.remove(platform)
        #blit all platforms
        for platform in self.platform_db:
            platform.blitIt()


#since our game is just a class
#the following creates an object of our game and runs its appropriate functions on execution
if __name__ == "__main__":
    myGame = Jumper()   #create a new instance of game Jumper
    myGame.run_game()   #run the game