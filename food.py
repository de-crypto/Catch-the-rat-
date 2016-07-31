#=============================================================================#
# Name        : food.py                                                       #
# Description : Food class definition for the snake game                      #
# Author      : Adrian Antonana                                               #
# Date        : 29.07.2012                                                    #
#=============================================================================#

# imports
import pygame as pg
import random as rnd
from colors import *

# block sizes
BLOCK_SIZE       = 30
BLOCK_SIZE_INNER = 20

# food class definition
class food:

	# class constructor
	def __init__(self,surface,minx,maxx,miny,maxy):
		self.surface = surface
		self.posx    = rnd.randint(minx,maxx-1)
		self.posy    = rnd.randint(miny,maxy-1)

		# for drawing the food
		self.foodblock = pg.Surface((BLOCK_SIZE,BLOCK_SIZE))
		self.foodblock.set_alpha(255)
		self.foodblock.fill(RED)
		self.foodblockdark = pg.Surface((BLOCK_SIZE_INNER,BLOCK_SIZE_INNER))
		self.foodblockdark.set_alpha(255)
		self.foodblockdark.fill(RED_DARK)

	# get food position
	def getPos(self):
		return (self.posx,self.posy)

	# draw the food
	def draw(self):
		fb = self.foodblock
		fbd = self.foodblockdark
		sf = self.surface

		# food is just two blocks
		foodpos = self.getPos()
		sf.blit(fb,(foodpos[1]*BLOCK_SIZE,foodpos[0]*BLOCK_SIZE))
		sf.blit(fbd,(foodpos[1]*BLOCK_SIZE+5,foodpos[0]*BLOCK_SIZE+5))
