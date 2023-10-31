# Importing modules: pygame and random
# Pygame, for pygame; Random for RNG-based functions
# Remember to `pip install -r requirements.txt`
import pygame, random

# Importing pygame.locals, for simplifying references
from pygame.locals import (
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	KEYDOWN,
	RLEACCEL,
	QUIT
)

# Pygame's Clock - used for game speed
clock = pygame.time.Clock()

# Player Class
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__() # Extending from pygame's built-in Sprite class

		"""
		Example code - in the case for Player being a basic rectangle.

		self.surf = pygame.Surface((75, 25))
		self.surf.fill((0, 0, 0))
		"""

		self.surf = pygame.image.load("catsprite.jpg").convert()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surf.get_rect()

	def update(self, pressed_keys):

		# Player movement - based on key presses
		if pressed_keys[K_UP]:
			self.rect.move_ip(0, -5)
		if pressed_keys[K_DOWN]:
			self.rect.move_ip(0, 5)
		if pressed_keys[K_LEFT]:
			self.rect.move_ip(-5, 0)
		if pressed_keys[K_RIGHT]:
			self.rect.move_ip(5, 0)

		# Player boundaries
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > screen_width:
			self.rect.right = screen_width
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= screen_height:
			self.rect.bottom = screen_height

# Enemy Class
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()

		"""
		Example code - making Enemy(s) small rectangles

		self.surf = pygame.Surface((20, 10))
		self.surf.fill((0, 255, 127)) # Color close to cyan-green
		"""

		self.surf = pygame.image.load("dogimage (1).jpg").convert()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surf.get_rect(center = # Setting the enemies' spawn location randomly
						(random.randint(screen_height + 20, screen_width + 100),
						 random.randint(0, screen_height)))
		self.speed = random.randint(5, 20) # Randomized speed, from 5 to 20

	def update(self): # The Enemy's update works differently than that of the Player's
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0: # Remove the sprite when it passes the left edge
			self.kill()

# Initializing Pygame
pygame.init()
running = True
font = pygame.font.Font("Roboto-Black.ttf", 15) # A Font object, used for the in-game timer display

# Setting up the Screen
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car's Magical Adventure!")

# Initializing a Player
player = Player()

# Enemy Spawn Custom Event
add_enemy = pygame.USEREVENT + 1
pygame.time.set_timer(add_enemy, 1000)	# Run the event `add_enemy` every `1` second

# 'Enemy' and 'All Sprite' Groups
enemies = pygame.sprite.Group()		# Enemies are used for collision and position updates
all_sprites = pygame.sprite.Group()	# Used to render (draw/place on screen)
all_sprites.add(player)

# Gameplay Loop
while running:

	# All events in pygame are stored in `pygame.event`
	# Each subsequent event is added into `pygame.event`
	for event in pygame.event.get():
		if event.type == KEYDOWN: # On key press
			if event.key == K_ESCAPE:
				running = False # On `Escape`, quit game
		if event.type == add_enemy:
			new_enemy = Enemy() 	# Creating a new Enemy
			enemies.add(new_enemy)	# Adding this `new_enemy` to the `enemies` group
			all_sprites.add(new_enemy)

	# Updating positions
	pressed_keys = pygame.key.get_pressed() # A dictionary of the pressed buttons
	player.update(pressed_keys)		# Updates Player positions, based on key presses
	enemies.update()			# Updating Enemy(s)

	# Special case - Check if the Player collided with any Enemy(s)
	if pygame.sprite.spritecollideany(player, enemies):
		player.kill()		# Remove the Player sprite (slightly redundant)
		running = False		# Quit the game

	# Rendering (Drawing)
	screen.fill((255, 255, 255))
	for entity in all_sprites:	# Cycle through all entities, and put them all to the screen
		screen.blit(entity.surf, entity.rect)

	# In-Game Timer
	seconds = int(pygame.time.get_ticks()/1000 % 60)
	text = font.render(str(seconds), True, (0, 0, 0))
	textRect = text.get_rect()
	textRect.center = (400 // 2, 400 // 2)
	screen.blit(text, (50, 50))

	# Put all to user's display!
	pygame.display.flip()

	# Game Running Speed
	clock.tick(60)			# Limits to 60 frames per second

"""
Example Code - How to Make a Surface

	# Making and defining a Surface
	surf = pygame.Surface((50, 50))	# Making a rectangle Surface
	surf.fill((0, 0, 0))		# Filling the rectangle Surface with black
	rect = surf.get_rect()		# Find the Surface's area

	# Positioning the Surface

	surf_center = (
		(screen_width - surf.get_width()) / 2,
		(screen_height - surf.get_height()) / 2
	)

	# Rendering the Surface

	screen.blit(surf, surf_center)	# .blit() takes a Surface, then draws another Surface on top
	pygame.display.flip()		# Update the screen, and push it to the user's display
"""
