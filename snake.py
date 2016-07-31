#==============================================================================================#
# Name        : snake.py                                                                       #
# Description : The snake class definition for the snake game.                                 #
# Author      : Adrian Antonana                                                                #
# Date        : 29.07.2012                                                                     #
#==============================================================================================#

# imports
import pygame as pg
from colors import *

# motion direction constants
UP    = 0
DOWN  = 1
LEFT  = 2
RIGHT = 3

# block sizes and colors
BLOCK_SIZE       = 30
BLOCK_SIZE_INNER = 20

# snake class definition
class snake:

	# constructor
	def __init__(self,surface,headposx=10,headposy=10):
		self.surface = surface
		self.length  = 10
		self.poslist = [(headposx,y) for y in reversed(range(headposy-self.length+1,headposy+1))]
		self.motdir  = RIGHT
		self.crashed = False

		# for drawing the snake
		self.snakeblock = pg.Surface((BLOCK_SIZE,BLOCK_SIZE))
		self.snakeblock.set_alpha(255)
		self.snakeblock.fill(GREEN)
		self.snakeblockdark = pg.Surface((BLOCK_SIZE_INNER,BLOCK_SIZE_INNER))
		self.snakeblockdark.set_alpha(255)
		self.snakeblockdark.fill(GREEN_DARK)

		# for removing the snake
		self.backblock = pg.Surface((BLOCK_SIZE,BLOCK_SIZE))
		self.backblock.set_alpha(255)
		self.backblock.fill(BLACK)

	# get snake's head position
	def getHeadPos(self):
		return (self.poslist[0])

	# get the motion direction
	def getMotionDir(self):
		return self.motdir

	# get the snake positions list
	def getPosList(self):
		return self.poslist

	# set the motion direction
	def setMotionDir(self,motdir):
		self.motdir = motdir

	# increase the snake length by one
	def incLength(self):
		self.length += 1

	# move the snake updates the positions list and checks if the snake has crashed
	def move(self):
		motdir = self.getMotionDir()
		headpos = self.getHeadPos()

		# update positions
		if motdir == UP:
			poslist = [(headpos[0]-1,headpos[1])]
		elif motdir == DOWN:
			poslist = [(headpos[0]+1,headpos[1])]
		elif motdir == LEFT:
			poslist = [(headpos[0],headpos[1]-1)]
		elif motdir == RIGHT:
			poslist = [(headpos[0],headpos[1]+1)]

		poslist.extend(self.poslist[:-1])
		self.poslist = poslist

		# check if crashed
		if self.getHeadPos() in self.getPosList()[1:]:
			self.crashed = True

	# check if the snake has crashed
	def chrashed(self):
		return self.crashed

	# grow the snake. add a new position at the end
	def grow(self):
		lastpos = self.getPosList()[-1]
		self.length += 1
		self.poslist.append((lastpos[0]-1,lastpos[1]))

	# draw the snake
	def draw(self):
		skb = self.snakeblock
		skbd = self.snakeblockdark
		sf = self.surface

		for blockpos in self.getPosList():
			sf.blit(skb,(blockpos[1]*BLOCK_SIZE,blockpos[0]*BLOCK_SIZE))
			sf.blit(skbd,(blockpos[1]*BLOCK_SIZE+5,blockpos[0]*BLOCK_SIZE+5))

	# delete the snake
	def remove(self):
		bkb = self.backblock
		sf = self.surface

		# draw block for every snake position
		for blockpos in self.getPosList():
			sf.blit(bkb,(blockpos[1]*BLOCK_SIZE,blockpos[0]*BLOCK_SIZE))
