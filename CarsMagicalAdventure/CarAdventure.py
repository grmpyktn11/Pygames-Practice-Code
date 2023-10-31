#we import the random class, we dont need to pip install cuz its inbuilt (refed in zybooks)
import random
# Importing the module for pygames, titled, pygames 
# to use this line, we first installed it in the terminal using the command:
#pip install pygame
import pygame

#Setting up pygame.locals, which are basically things that make referencing stuff ez
#in this case, we are using keys, which quickly references keys

from pygame.locals import(

    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    RLEACCEL, #this makes pygames render (put things on screen) faster 
    QUIT,
)

## this is the clock where we run everything based off of
clock = pygame.time.Clock()

#in this section, we will make a player Class.
class Player(pygame.sprite.Sprite):
    def __init__(self):
        ##here, we give it a surface, and we color in the surface + get the dimentions
        super(Player, self).__init__()
        '''
        if we want to make the player a basic rectangle, we can use this
        but we decided to make it a photo of a car
        self.surf = pygame.Surface((75,25))
        self.surf.fill((0,0,0))
        '''
        self.surf = pygame.image.load("catsprite.jpg").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

         # Keep player on the screen
        '''        
        #what we're doing is making sure the player doesnt go too left off the canvas
        or too right, then same with up and down (0 < y < height)
        '''
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

#similar to the player class and its functions, we now make an enemy class

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        '''this would create a small rectangle for our enemy
        self.surf = pygame.Surface((20, 10)) 
        self.surf.fill((0, 255, 127)) #different color
        '''
        self.surf = pygame.image.load("dogimage (1).jpg").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=( ##the enemy actually spawns at a random location instead of set one
                random.randint(screen_height + 20, screen_width + 100),
                random.randint(0, screen_height),
            )
        )
        self.speed = random.randint(5, 20) #the enemy will have a speed thats between 5 and 20
   
    def update(self): #the enemy class' update works differently
        self.rect.move_ip(-self.speed, 0)   # Move the sprite based on speed
        # Remove the sprite when it passes the left edge of the screen
        if self.rect.right < 0:
            self.kill() 
            
#now, we set up the window we'll be workingin.
##these constants represent size
screen_width = 1080
screen_height = 720


#now that we're all set up, we can initialize the program (make the game and winodws start)
pygame.init()




#now we have to create the actual screen, reporesented by the screen variable
screen = pygame.display.set_mode((screen_width, screen_height)) 


#here, we made a custom event for adding a new enemy. defined under the events loop.
add_enemy = pygame.USEREVENT + 1
pygame.time.set_timer(add_enemy, 1000) #every second, run this event

#making the windows name
pygame.display.set_caption("car's magical adventure")

#here, we initialized a player instance
player = Player()

##we created a surface for a timer
font = pygame.font.Font('Roboto-Black.ttf', 15)
# create a text surface object,
# on which text is drawn on it.



#now we will make a sprite group for the enemies, and one for all the sprites in game
 
# - all_sprites is used for rendering
enemies = pygame.sprite.Group() #used for collision detection and position updates
all_sprites = pygame.sprite.Group() #used for rendering (placing things on the screen)

all_sprites.add(player) #we add the player we initialized on line 91 to the group


#now, we set up the actual loop for how long the game is, basically until user quits
#variable to represent status of the game
running = True

#now, the gameplay loop

while running:

    #now, all the events are stored in a list called pygame.event, it adds one everytime you get one
    for event in pygame.event.get(): ##itereating through the most recent event,

        if event.type == KEYDOWN: #if a key is pressed

            if event.key == K_ESCAPE: #if that key happens to be escape
                running = False #turn the game loop off. 
            
        # Add a new enemy
        elif event.type == add_enemy:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy() #creates a default enemy
            enemies.add(new_enemy) #adds it to the group of enemies
            all_sprites.add(new_enemy) #adds it to all the sprites  

    # This allows us to get a dictonary of the current pressed button(s)
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    #now update the enemy's position
    enemies.update()

    #we want to make the background white, so we will fill the screen (think paint bucket)
    screen.fill((255, 255, 255))

    
    




    #now we can put all the sprites in the group on the screen
    for entity in all_sprites: #for everything stored int he
        screen.blit(entity.surf, entity.rect) #put it on the screen

    seconds = int(pygame.time.get_ticks()/1000 %60)

   
    text = font.render(str(seconds),True, (0,0,0))
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (400 // 2, 400 // 2)
    


    screen.blit(text, (50,50))


    
    #display it
    pygame.display.flip()

    


   

    # Ensure program maintains a rate of 60 frames per second
    clock.tick(60)
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies): #if the player, hits anything in enemies
        player.kill() #kill :3
        running = False #end the game


'''

These is a way to make a surface, one way to draw things on the screen

    #now, we can make a block, this will be made using Surface.
    ##surface is a rectangle 50x50
    surf = pygame.Surface((50,50))

    ###adding a color to the surface, (0,0,0) RGB is always black
    surf.fill((0, 0, 0))
    rect = surf.get_rect()
    
    #now, we place the rectangle onto a surface, this being the screen. 
    # Put the center of surf at the center of the display
   
    ##since by default the coordinaates given to .blit are where you want to put 
    the top left of the surface, we have to adjust to center our rectangle.
 
    surf_center = (
        (screen_width-surf.get_width())/2,
        (screen_height-surf.get_height())/2
    )
    
    # Draw surf at the new coordinates
    screen.blit(surf, surf_center) #.blit takes a target surface, then adds another surface on it
    pygame.display.flip() #updates the screen and shows our rectangle
'''




