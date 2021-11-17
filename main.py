from ntpath import join
import pygame
from pygame.locals import *
import os
import sys

from pygame.transform import scale

pygame.init()
pygame.mixer.init()

motion = "stop"

screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('Endlace')

clock = pygame.time.Clock()
allSprites = pygame.sprite.Group()

### Настраиваем директории ###
rootPath = os.path.dirname(__file__)
resourcesPath = os.path.join(rootPath, "resources")
texturesPath = os.path.join(resourcesPath, "textures")
playerPath = os.path.join(texturesPath, "player")
skinsPath = os.path.join(playerPath, "skins")
defaultIdle = os.path.join(skinsPath, "default-idle")
defaultRun = os.path.join(skinsPath, "default-run")

### Настраиваем пути текстур ###
ground512 = pygame.image.load(os.path.join(texturesPath, "ground512x512.png"))
box = pygame.image.load(os.path.join(texturesPath, "normalbox.png"))
box = pygame.transform.scale(box, (64, 64))
playerShadow = pygame.image.load(os.path.join(playerPath, "shadow.png"))
playerShadow = pygame.transform.scale(playerShadow, (64,64))
boxSprite = pygame.sprite.Sprite()
boxSprite.image = box
boxSprite.rect = box.get_rect()

### Настраиваем шрифт ###
font1 = pygame.font.Font('font.ttf', 36)

grid1 = pygame.Rect((0,0,64,64))
fakeScreen = screen.copy()
testSurface = pygame.Surface((512,512))

screenScrollX = 0
screenScrollY = 0

frameCount = 0

mapList = [[[0,0,0,0,0,0,0,0], #layer 1
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0]],
			   
		   [[0,0,0,0,0,0,0,0], #layer 2
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0]],
			   
		   [[0,0,0,0,0,0,0,0], #layer 3
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0]],
			   
		   [[0,0,0,0,0,0,0,0], #layer 4
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0],
		   	[0,0,0,0,0,0,0,0]],]

### Классы ###
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(defaultIdle, "frame1.png"))
		self.image = pygame.transform.scale(self.image, (64, 64))
		self.rect = self.image.get_rect()
		self.rect.center = (128,128)


	def moveRight(self):
		global screenScrollX
		if not self.rect.right > 512:
			self.rect.x += 4
			# screenScrollX -= 8
	
	def moveLeft(self):
		global screenScrollX
		if not self.rect.left < 0:
			self.rect.x -= 4
			# screenScrollX += 8
	
	def moveUp(self):
		global screenScrollY
		if not self.rect.top < 0:
			self.rect.y -= 4
			# screenScrollY += 8
	
	def moveDown(self):
		global screenScrollY
		if not self.rect.bottom > 512:
			self.rect.y += 4
			# screenScrollY -= 8
	
	def moveLeftDown(self):
		global screenScrollX, screenScrollY
		if not self.rect.bottom > 512:
			if not self.rect.left < 0:
				self.rect.y += 4
				# screenScrollY -= 8
				self.rect.x -= 4
				# screenScrollX += 8

	def moveLeftUp(self):
		global screenScrollX, screenScrollY
		if not self.rect.top < 0:
			if not self.rect.left < 0:
				self.rect.y -= 4
				# screenScrollY += 8
				self.rect.x -= 4
				# screenScrollX += 8

	def moveRightDown(self):
		global screenScrollX, screenScrollY
		if not self.rect.bottom > 512:
			if not self.rect.right > 512:
				self.rect.y += 4
				# screenScrollY -= 8
				self.rect.x += 4
				# screenScrollX -= 8

	def moveRightUp(self):
		global screenScrollX, screenScrollY
		self.rect.y -= 4
		# screenScrollY += 8
		self.rect.x += 4
		# screenScrollX -= 8


player = Player()
allSprites.add(player)

def mainMenu():
	while True:
		clock.tick(60)

		screen.fill((0,0,0))

		posX, posY = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		
		pygame.display.flip()

def sandbox():
	global motion
	global frameCount
	while True:
		clock.tick(60)
		
		screen.fill((0,0,0))

		posX, posY = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYUP:
				motion = "stop"
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					boxSprite = pygame.sprite.Sprite()
					boxSprite.image = box
					boxSprite.rect = box.get_rect()
					print(int(posX/64))
					print(int(posY/64))
					clickX = int(posX/64)
					clickY = int(posY/64)
					# if mapList[0][clickX][clickY] == 1:
					# 	mapList[1][clickX][clickY] = 1
					# 	boxSprite.rect.x = (posX//64)*64
					# 	boxSprite.rect.y = (posY//64)*64-28
					# 	print(mapList)
					# 	allSprites.add(boxSprite)
					# elif mapList[1][clickX][clickY] == 1:
					# 	mapList[2][clickX][clickY] = 1
					# 	boxSprite.rect.x = (posX//64)*64-58
					# 	print(mapList)
					# 	allSprites.add(boxSprite)
					# elif mapList[2][clickX][clickY] == 1:
					# 	mapList[3][clickX][clickY] = 1
					# 	boxSprite.rect.x = (posX//64)*64-678
					# 	print(mapList)
					# 	allSprites.add(boxSprite)
					# else:
					# 	mapList[0][clickX][clickY] = 1
					# 	boxSprite.rect.x = (posX//64)*64
					# 	boxSprite.rect.y = (posY//64)*64
					# 	print(mapList)
					# 	allSprites.add(boxSprite)
					mapList[0][clickX][clickY] = 1
					boxSprite.rect.x = (posX//64)*64
					boxSprite.rect.y = (posY//64)*64
					# print(mapList)
					allSprites.add(boxSprite)
				
		keys = pygame.key.get_pressed()
		
		if frameCount + 1 >= 27:
			frameCount = 0

		#moving
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			motion = "left"
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			motion = "right"
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			motion = "up"
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			motion = "down"
		if keys[pygame.K_LEFT] and keys[K_UP]:
			motion = "leftup"
		if keys[pygame.K_LEFT] and keys[K_DOWN]:
			motion = "leftdown"
		if keys[pygame.K_RIGHT] and keys[K_UP]:
			motion = "rightup"
		if keys[pygame.K_RIGHT] and keys[K_DOWN]:
			motion = "rightdown"

		if motion == "left":
			player.moveLeft()
			# fakeScreen.blit(player.images[frameCount//3], (player.rect.x,player.rect.y))
			# frameCount += 1
		if motion == "right":
			player.moveRight()
			# fakeScreen.blit(player.images[frameCount//3], (player.rect.x,player.rect.y))
			# frameCount += 1
		if motion == "up":
			player.moveUp()
			# fakeScreen.blit(player.images[frameCount//3], (player.rect.x,player.rect.y))
			# frameCount += 1
		if motion == "down":
			player.moveDown()
			# fakeScreen.blit(player.images[frameCount//3], (player.rect.x,player.rect.y))

		if motion == "leftup":
			player.moveLeftUp()
		if motion == "leftdown":
			player.moveLeftDown()
		if motion == "rightup":
			player.moveRightUp()
		if motion == "rightdown":	
			player.moveRightDown()

		if motion == "stop":
			pass
	
		# screen.blit(player, (0,0))
		fakeScreen.blit(ground512, (0,0))
		fakeScreen.blit(playerShadow, (player.rect.x, player.rect.y))
		allSprites.update()
		allSprites.draw(fakeScreen)
		text2 = font1.render(str(int(clock.get_fps())), False,
                  (255, 255, 255))
		fakeScreen.blit(text2, (0,0))
		screen.blit(pygame.transform.scale(fakeScreen, (512, 512)), (screenScrollX,screenScrollY))
		pygame.display.flip()

sandbox()
