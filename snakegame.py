#===============================================================================================#
# Name        : snakegame.py                                                                    #
# Description : Python version of the snake game.                                               #
# Author      : Adrian Antonana                                                                 #
# Date        : 29.07.2012                                                                      #
#===============================================================================================#

# imports
import pygame as pg
import snake as snk
import food as fd
import sys
from colors import *

# screen size and game speed
WIDTH      = 25
HEIGHT     = 25
SPEED      = 8
SPEED_TICK = 2
SPEED_INC  = 5
SHORT      = 12
LONG       = 1

# defining the outer wall blocks
wallblock = pg.Surface((snk.BLOCK_SIZE,snk.BLOCK_SIZE))
wallblock.set_alpha(255)
wallblock.fill(BLUE)
wallblockdark = pg.Surface((snk.BLOCK_SIZE_INNER,snk.BLOCK_SIZE_INNER))
wallblockdark.set_alpha(255)
wallblockdark.fill(BLUE_DARK)

#================================================================================================#
#                                       Function Definitions                                     #
#================================================================================================#

# check if the snake's head is outside the limits
def inLimits(snake):
	headpos = snake.getHeadPos()
	return not (headpos[0] < 1 or headpos[1] < 1 or headpos[0] >= HEIGHT+1 or headpos[1] >= WIDTH+1)

# draw walls
def drawWalls(surface):

	# left and right walls
	for y in range(HEIGHT+1):
		surface.blit(wallblock,(0,y*snk.BLOCK_SIZE))
		surface.blit(wallblockdark,(5,y*snk.BLOCK_SIZE+5))
		surface.blit(wallblock,((WIDTH+1)*snk.BLOCK_SIZE,y*snk.BLOCK_SIZE))
		surface.blit(wallblockdark,((WIDTH+1)*snk.BLOCK_SIZE+5,y*snk.BLOCK_SIZE+5))

	# upper and bottom walls
	for x in range(WIDTH+2):
		surface.blit(wallblock,(x*snk.BLOCK_SIZE,0))
		surface.blit(wallblockdark,(x*snk.BLOCK_SIZE+5,5))
		surface.blit(wallblock,(x*snk.BLOCK_SIZE,(HEIGHT+1)*snk.BLOCK_SIZE,))
		surface.blit(wallblockdark,(x*snk.BLOCK_SIZE+5,(HEIGHT+1)*snk.BLOCK_SIZE+5))

#================================================================================================#
#                                       Main Game Part                                           #
#================================================================================================#

# initialize pygame, clock for game speed and screen to draw
pg.init()

# initializing mixer, sounds, clock and screen
pg.mixer.init()
eatsound = pg.mixer.Sound("snakeeat.wav")
crashsound = pg.mixer.Sound("snakecrash.wav")
clock = pg.time.Clock()
screen = pg.display.set_mode(((WIDTH+2)*snk.BLOCK_SIZE,(HEIGHT+2)*snk.BLOCK_SIZE))
pg.display.set_caption("snake")
font = pg.font.SysFont(pg.font.get_default_font(),40)
gameovertext = font.render("GAME OVER",1,WHITE)
starttext = font.render("PRESS ANY KEY TO START",1,WHITE)
screen.fill(BLACK)

# we need a snake and something to eat
snake = snk.snake(screen,WIDTH/2,HEIGHT/2)
food = fd.food(screen,1,HEIGHT+1,1,WIDTH+1)

# food should not appear where the snake is
while food.getPos() in snake.getPosList():
	food.__init__(screen,1,HEIGHT+1,1,WIDTH+1)

# only queue quit and and keydown events
# pg.event.set_allowed([pg.QUIT,pg.KEYDOWN])
pg.event.set_blocked([pg.MOUSEMOTION,pg.MOUSEBUTTONUP,pg.MOUSEBUTTONDOWN])

# will increase game speed every 10 times we eat
eaten = 0

# press any key to start!!!
drawWalls(screen)
screen.blit(starttext,((WIDTH-10)*snk.BLOCK_SIZE/2,HEIGHT*snk.BLOCK_SIZE/2))
pg.display.flip()
waiting = True
while waiting:
	event = pg.event.wait()
	if event.type == pg.KEYDOWN:
		waiting = False
screen.fill(BLACK)

# main loop
running = True
while running:

	# check crash or move outside the limits
	if not inLimits(snake) or snake.crashed:
		running = False
		crashsound.play()
	else:

		# draw screen with snake and foods
		food.draw()
		snake.draw()
		drawWalls(screen)
		pg.display.flip()

		# check if snake eates
		if food.getPos() == snake.getHeadPos():
			eatsound.play()
			snake.grow()
			# food should not appear where the snake is
			food.__init__(screen,1,HEIGHT+1,1,WIDTH+1)
			while food.getPos() in snake.getPosList():
				food.__init__(screen,1,HEIGHT+1,1,WIDTH+1)
			eaten += 1
			# increase game speed
			if eaten % SPEED_INC == 0:
				SPEED += SPEED_TICK

		# game speed control
		clock.tick(SPEED)

		# get the next event on queue
		event = pg.event.poll()
		if event.type == pg.QUIT:
			sys.exit()
		elif event.type == pg.KEYDOWN:
			actmotdir = snake.getMotionDir()
			if event.key == pg.K_ESCAPE:
				sys.exit()
			elif event.key == pg.K_UP and actmotdir != snk.DOWN:
				snake.setMotionDir(snk.UP)
			elif event.key == pg.K_DOWN and actmotdir != snk.UP:
				snake.setMotionDir(snk.DOWN)
			elif event.key == pg.K_RIGHT and actmotdir != snk.LEFT:
				snake.setMotionDir(snk.RIGHT)
			elif event.key == pg.K_LEFT and actmotdir != snk.RIGHT:
				snake.setMotionDir(snk.LEFT)

		# remove the snake and make movement
		snake.remove()
		snake.move()

# if crashed print "game over" and wait for esc key
clock.tick(LONG)
snake.draw()
drawWalls(screen)
snakeposlist = snake.getPosList()
blackblock = snake.backblock
for pos in snakeposlist[1:]:
	screen.blit(blackblock,(pos[1]*snk.BLOCK_SIZE,pos[0]*snk.BLOCK_SIZE))
	pg.display.flip()
	clock.tick(SHORT)

while True:
	screen.blit(gameovertext,((WIDTH-4)*snk.BLOCK_SIZE/2,HEIGHT*snk.BLOCK_SIZE/2))
	pg.display.flip()
	event = pg.event.wait()
	if event.type == pg.KEYDOWN:
		if event.key == pg.K_ESCAPE:
			sys.exit()
