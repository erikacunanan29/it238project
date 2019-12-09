import pygame
import threading
from threading import Timer

#Loaded images - tanks, bullets, map elements
left = pygame.image.load('Images/leftTank.jpg')
right = pygame.image.load('Images/rightTank.jpg')
up = pygame.image.load('Images/upTank.jpg')
down = pygame.image.load('Images/downTank.jpg')

downBullet = pygame.image.load('Images/downBullet.png')
leftBullet = pygame.image.load('Images/leftBullet.png')
rightBullet = pygame.image.load('Images/rightBullet.png')
upBullet = pygame.image.load('Images/upBullet.png')

mapBrick = pygame.image.load('Images/map_Brick.jpg')
mapSteel = pygame.image.load('Images/map_Steel.jpg')
mapGrass = pygame.image.load('Images/map_Grass.jpg')
mapWater = pygame.image.load('Images/map_Water.jpg')

explode = pygame.image.load('Images/explode.jpg')
 
#---------------------------------- CLASS TANK ---------------------------------- #

class Tank(object):
	def __init__(self, nickname, x, y):
		self.nickname = nickname
		self.x = x
		self.y = y
		self.width = 30
		self.height = 30
		self.vel = 5

		#Determines which side the tank is facing
		self.leftSide = True
		self.rightSide = False
		self.upSide = False
		self.downSide = False

		#Checks whether the tank has fired a bullet
		self.firedBullet = False

		#Checks whether the tank has been hit
		self.enemyHit = False

		#Computes the total points garnered by the player
		self.totalPoints = 0

		#Gets the bounding box for collision - left, top, right, bottom
		self.hitbox = (self.x, self.y, self.width, self.height) 

	def drawObject(self, window):
		if self.enemyHit: #If the tank is hit, render the explode sprite
			window.blit(explode, (self.x, self.y))
		else: #If the tank is simply moving, render the tank with appropriate direction
			if self.leftSide:
				window.blit(left, (self.x, self.y))
			elif self.rightSide:
				window.blit(right, (self.x, self.y))
			elif self.upSide:
				window.blit(up, (self.x, self.y))
			elif self.downSide:
				window.blit(down, (self.x, self.y))

	#Function that sets the current direction the tank is facing during the movement
	def setDirection(self, direction): 
		self.leftSide = False
		self.rightSide = False
		self.upSide = False
		self.downSide = False

		if direction == 'L':
			self.leftSide = True
		elif direction == 'R':
			self.rightSide = True
		elif direction == 'U':
			self.upSide = True
		elif direction == 'D':
			self.downSide = True

	#Function that resets variables of a tank after it has been hit
	def respawn(self):
		self.enemyHit = False
		self.leftSide = True
		window.blit(left, (self.x, self.y))

#---------------------------------- CLASS BULLET  ---------------------------------- #

class Bullet(object):
	def __init__(self, x, y, facing):
		self.x = x
		self.y = y
		self.facing = facing
		self.vel = 10

	#Function that renders the bullet depending on the direction the tank is facing
	def drawObject(self, window):
		if self.facing == 'L':
			window.blit(leftBullet, (self.x, self.y))
		elif self.facing == 'R':
			window.blit(rightBullet, (self.x, self.y))
		elif self.facing == 'U':
			window.blit(upBullet, (self.x, self.y))
		elif self.facing == 'D':
			window.blit(downBullet, (self.x, self.y))

#---------------------------------- CLASS MAP ---------------------------------- #

class Map(object): #Supposed to be for setting up the map but the map template is still missing
	def __init__(self, x, y, element):
		self.x = x
		self.y = y
		self.element = element
		self.state = [] #Can be crossed, can be broken, can bullets pass through

	def drawObject(self, window):
		if self.element == '#': #bricks #
			window.blit(mapBrick, (self.x, self.y))
			self.state = [False, True, False]
		elif self.element == '@': #steel walls @
			window.blit(mapSteel, (self.x, self.y))
			self.state = [False, False, False]
		elif self.element == '%': #bush %
			window.blit(mapGrass, (self.x, self.y))
			self.state = [True, False, True]
		elif self.element == '~': #water ~
			window.blit(mapWater, (self.x, self.y))
			self.state = [False, False, True]

#---------------------------------- MAIN FUNCTIONALITY ---------------------------------- #

#Renders the tally of the scores of the players
def highscores():
	pygame.draw.rect(window, (167, 158, 159), (1000, 0, 250, 700))
	startY = 75

	font = pygame.font.SysFont("Trebuchet MS", 30, True)

	text = font.render("SCOREBOARD", 1, (0, 0, 0))
	window.blit(text, (1035, 25))

	for player in players:
		name = font.render(player.nickname, 1, (0, 0, 0))
		score = font.render(str(player.totalPoints), 1, (0, 0, 0))
		
		window.blit(name, (1040, startY))
		window.blit(score, (1155, startY))

		startY += 45

#Re-draws the window to display the updates of the game
def redrawGameWindow():
	window.fill((0, 0, 0))

	highscores()

	for element in mapElements:
		element.drawObject(window)

	for player in players:
		player.drawObject(window)

		if player.enemyHit:
			t = Timer(5, player.respawn)
			t.start()

	for bullet in bullets:
		bullet.drawObject(window)

	pygame.display.update()


#Initializes the game with proper screen size, and caption
pygame.init()

screenWidth = 1000
screenHeight = 700

window = pygame.display.set_mode((screenWidth+250, screenHeight))
pygame.display.set_caption("Battle City")

#Setup the map given a template
mapElements = []

fileHandle = open("Maps/map1.txt", "r")

i=0
j=0
for line in fileHandle: #Gets every element from the file
	j = 0
	for c in line:
		if c != '.': #If element is a map element
			mapElements.append(Map(j, i, c)) #Append it to the map elements array
		j += 30
	i += 30

#Initializes the current player
currentPlayer = Tank("F", 50, 50)

#Creates an array for the storage of the bullets and the players available
bullets = []
players = []

#Appends 6 players to the array
players.append(currentPlayer)
players.append(Tank("A", 150, 150))
players.append(Tank("B", 300, 300))
players.append(Tank("C", 400, 400))
players.append(Tank("D", 500, 500))
players.append(Tank("E", 600, 600))

run = True

while run:
	pygame.time.delay(50)

	#Checks if the user has exitted the program
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	#For every bullet that is shot in the game
	for bullet in bullets:
		for player in players:
			if player != currentPlayer: #Checks if the bullet has hit a player
				if bullet.y < player.hitbox[1] + player.hitbox[3] and bullet.y > player.hitbox[1]:
					if bullet.x > player.hitbox[0] and bullet.x < player.hitbox[0] + player.hitbox[2]:
						if player.enemyHit != True: #If a bullet has hit a player
							currentPlayer.totalPoints += 100 #The attacker will get points for defeating the enemy
							player.enemyHit = True #Tells the attacked tank that it has been defeated
							bullets.pop(bullets.index(bullet))

		#Checks if the bullet has exceeded the minimum maximum boundaries of the screen
		if bullet.x < screenWidth-30 and facing == 'R' and bullet.x > 0:
			bullet.x += bullet.vel
		elif bullet.x > 0 and facing == 'L':
			bullet.x -= bullet.vel
		elif bullet.y < screenHeight and facing == 'D' and bullet.y > 0:
			bullet.y += bullet.vel
		elif bullet.y > 0 and facing == "U":
			bullet.y -= bullet.vel
		else:
			bullets.pop(bullets.index(bullet))

	keys = pygame.key.get_pressed() #Determines which keys are pressed

	#If the player has shot a bullet
	if keys[pygame.K_SPACE] and (currentPlayer.firedBullet == False or len(bullets) == 0):
		if currentPlayer.leftSide:
			facing = 'L'
		elif currentPlayer.rightSide:
			facing = 'R'
		elif currentPlayer.upSide:
			facing = 'U'
		elif currentPlayer.downSide:
			facing = 'D'

		if (len(bullets) < 1):
			bullets.append(Bullet(round(currentPlayer.x+currentPlayer.height//2), round(currentPlayer.y+currentPlayer.width//2), facing))
			currentPlayer.firedBullet = True

	#If the player has moved to either up, down, left, right
	if keys[pygame.K_LEFT] and currentPlayer.x > currentPlayer.vel:
		currentPlayer.x -= currentPlayer.vel
		currentPlayer.setDirection('L')
	elif keys[pygame.K_RIGHT] and currentPlayer.x < (screenWidth - currentPlayer.width - currentPlayer.vel):
		currentPlayer.x += currentPlayer.vel
		currentPlayer.setDirection('R')
	elif keys[pygame.K_UP] and currentPlayer.y > currentPlayer.vel:
		currentPlayer.y -= currentPlayer.vel
		currentPlayer.setDirection('U')
	elif keys[pygame.K_DOWN] and currentPlayer.y < (screenHeight - currentPlayer.height - currentPlayer.vel):
		currentPlayer.y += currentPlayer.vel
		currentPlayer.setDirection('D')

	redrawGameWindow()

pygame.quit()