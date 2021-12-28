import cgitb 
cgitb.enable()
from math import gamma
import pygame
import random
import os
from pygame import mixer
from spritesheet import SpriteSheet
from enemy import Enemy
import sys

# This is for pyinstaller (making an exe)
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#initialise pygame
mixer.init()
pygame.init()

#game window dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy')

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#load music and sounds
pygame.mixer.music.load('assets/music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0)
eat_fx = pygame.mixer.Sound('assets/eat.mp3')
eat_fx.set_volume(1)


#game variables
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

if os.path.exists('score.txt'):
	with open('score.txt', 'r') as file:
		high_score = int(file.read())
else:
	high_score = 0

#define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)

#define font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

#load images
jumpy_image = pygame.image.load('assets/hugo.png').convert_alpha()
bg_image = pygame.image.load('assets/bg.png').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (1200, 800))
	#birds
bird_sheet_img = pygame.image.load('assets/Frikandel.png').convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img)
#create enemy groups
enemy_group = pygame.sprite.Group()

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#function for drawing info panel
def draw_panel():
	pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
	pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
	draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 0)


#function for drawing the background
def draw_bg(bg_scroll):
	screen.blit(bg_image, (0, 0 + bg_scroll))
	screen.blit(bg_image, (0, -600 + bg_scroll))

#player class
class Player():
	def __init__(self, x, y):
		self.image = pygame.transform.scale(jumpy_image, (120, 170))
		self.width = 25
		self.height = 40
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x, y)
		self.vel_y = 0
		self.flip = False
		self.jump = False

	def move(self):
		#reset variables
		scroll = 0
		dx = 0
		dy = 0

		#process keypresses
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			dx = -10
			self.flip = True
		if key[pygame.K_d]:
			dx = 10
			self.flip = False
		if key[pygame.K_SPACE]:
			dy = -20
			self.jump = True

		#gravity
		self.vel_y += GRAVITY
		dy += self.vel_y

		#ensure player doesn't go off the edge of the screen
		if self.rect.left + dx < 0:
			dx = -self.rect.left
		if self.rect.right + dx > SCREEN_WIDTH:
			dx = SCREEN_WIDTH - self.rect.right


		#check collision with ground
		if self.rect.bottom + dy > SCREEN_HEIGHT - 350:
			dy = 0
			self.vel_y = 0

		#update rectangle position
		self.rect.x += dx
		self.rect.y += dy

		#update mask
		self.mask = pygame.mask.from_surface(self.image)



	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))


jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 600)

#game loop
run = True
while run:

	clock.tick(FPS)
	jumpy.move()
	
	#check if game is over
	if game_over == False:
		

	#generate enemies
		if len(enemy_group) == 0 or score > 1500:
			enemy = Enemy(SCREEN_WIDTH, 310, bird_sheet, 1.5)
			enemy_group.add(enemy)
	#update enemies
		enemy_group.update(scroll, SCREEN_WIDTH)

	#check for collision with enemies
		if pygame.sprite.spritecollide(jumpy, enemy_group, True):
			eat_fx.play()
			score = score + 1
			game_over = False



	#draw background
	screen.blit(bg_image, (0, 0))

	#draw sprites
	enemy_group.draw(screen)
	jumpy.draw()

	#draw panel
	draw_panel()


	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


	#update display window
	pygame.display.update()



pygame.quit()

