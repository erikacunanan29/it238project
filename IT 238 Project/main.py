import pygame
import threading
import random
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
mapBlank = pygame.image.load('Images/map_Blank.jpg')

explode = pygame.image.load('Images/explode.jpg')
vanish = pygame.image.load('Images/vanish.jpg')

#---------------------------------- CLASS TANK ---------------------------------- #

class Tank(object):
	def __init__(self, nickname, x, y):
		self.nickname = nickname
		self.x = x
		self.y = y
		self.width = 30
		self.height = 30
		self.vel = 30

		#Determines which side the tank is facing
		self.leftSide = True
		self.rightSide = False
		self.upSide = False
		self.downSide = False

		#Checks whether the tank has fired a bullet
		self.firedBullet = False

		#Checks whether the tank has been hit
		self.enemyHit = False
		self.state = True

		#Computes the total points garnered by the player
		self.totalPoints = 0

		#Gets the bounding box for collision - left, top, right, bottom
		self.hitbox = (self.x, self.y, self.width, self.height) 

	def drawObject(self, window):
		if self.enemyHit: #If the tank is hit, render the explode sprite
			#window.blit(explode, (self.x, self.y))
			window.blit(vanish, (self.x, self.y))
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
		self.state = True 
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
		self.hitbox = (self.x, self.y, 30, 28) # sets bounding box for the map


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

	for player in players:
		player.drawObject(window)
		#commented out respawn to test game over
		#if player.enemyHit:
		#	t = Timer(5, player.respawn)
		#	t.start()

	for bullet in bullets:
		bullet.drawObject(window)

	for element in mapElements:
		element.drawObject(window)


	pygame.display.update()

#Show Game over Screen and project the winner
def show_game_over(win):

	background = pygame.Surface(window.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	font = pygame.font.Font(None, 36)
	text = font.render("Game Over! "+win+" is the winner!", 1, (10, 10, 10))
	textpos = text.get_rect(center=(screenWidth/2, screenHeight/2))
	background.blit(text, textpos)

	window.blit(background, (0, 0))
	pygame.display.flip()

	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()




#Collision detections
def Collision(curx, cury):
	isBrick = False
	isMetal = False
	isWater = False
	isGrass = False
	element = ""

	if mapData[cury][curx] == '#':
		element = "Brick"
	if mapData[cury][curx] == '@':
		element = "Metal"
	if mapData[cury][curx] == '~':
		element = "Water"
	if mapData[cury][curx] == '%':
		element = "Grass"	
	return element

#Initializes the game with proper screen size, and caption
pygame.init()

screenWidth = 1000
screenHeight = 700

window = pygame.display.set_mode((screenWidth+250, screenHeight))
pygame.display.set_caption("Battle City")
rand = [1,2,3]
map_no = random.choice(rand)
print(map_no)
filename = ('Maps/map'+str(map_no)+'.txt')
print(filename)
#Setup the map given a template
mapElements = []
fileHandle = open(filename, "r")

i=0
j=0
for line in fileHandle: #Gets every element from the file
	j = 0
	for c in line:
		# if c != '.': #If element is a map element
		mapElements.append(Map(j, i, c)) #Append it to the map elements array
		j += 30
	i += 30


#Initializes a random position for the current player
mapData = []
f = open(filename, "r")
for line in f:
	mapData.append(line)
isBlank = False
while not isBlank:
	ycol = random.randint(0,33)
	xrow = random.randint(0,21)
	if mapData[xrow][ycol] == '.':
		isBlank = True
		currentPlayer = Tank("F", ycol*30, xrow*30)

#Creates an array for the storage of the bullets and the players available
bullets = []
players = []

#Appends 6 players to the array
players.append(currentPlayer)
players.append(Tank("A", 100, 100))
players.append(Tank("B", 300, 300))
players.append(Tank("C", 210, 210))
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
							player.state = False #set the state of the Player to inactive since it has been hit
							#print('player removed')

 		#Checks if bullet hit an element
		for i in range(0, len(mapElements)):
			if mapElements[i].element == '#':
				if bullet.y < mapElements[i].hitbox[1] + mapElements[i].hitbox[3] and bullet.y > mapElements[i].hitbox[1]:
					if bullet.x > mapElements[i].hitbox[0] and bullet.x < mapElements[i].hitbox[0] + mapElements[i].hitbox[2]:
						bullets.pop(bullets.index(bullet))
						mapElements[i].element = '.'
						print("bullet hit a brick")
			elif mapElements[i].element == '@':
				if bullet.y < mapElements[i].hitbox[1] + mapElements[i].hitbox[3] and bullet.y > mapElements[i].hitbox[1]:
					if bullet.x > mapElements[i].hitbox[0] and bullet.x < mapElements[i].hitbox[0] + mapElements[i].hitbox[2]:
						bullets.pop(bullets.index(bullet))
						mapElements[i].element = '.'
						print("bullet hit steel")
			else:
				continue
		
		
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

	k = 0
	winner ={}
	#get active players
	for player in players:
		if player.state == True:
			k = k+1
			winner.update({player.nickname:player.totalPoints})
	#if there is only one active player he/she is the winner, game ends
	if k == 1:
		#print(winner)
		champion = list(winner.keys())
		print(champion)
		print('Game Over, you win!')
		run = False	
		show_game_over(champion[0])


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
		curx = int((currentPlayer.x-30)/30)
		cury = int((currentPlayer.y)/30)
		collisionWith = Collision(curx, cury)
		print(collisionWith)
		if collisionWith != "Brick" and collisionWith != "Metal" and collisionWith != "Water" :
			currentPlayer.x -= currentPlayer.vel
			if collisionWith == "Grass":
				print("Hide under")
				window.blit(mapGrass, (currentPlayer.x, currentPlayer.y))
		currentPlayer.setDirection('L')
	elif keys[pygame.K_RIGHT] and currentPlayer.x < (screenWidth - currentPlayer.width - currentPlayer.vel):
		curx = int((currentPlayer.x+30)/30)
		cury = int((currentPlayer.y)/30)
		collisionWith = Collision(curx, cury)
		print(collisionWith)
		if collisionWith != "Brick" and collisionWith != "Metal" and collisionWith != "Water" :
			currentPlayer.x += currentPlayer.vel
			if collisionWith == "Grass":
				print("Hide under")
				window.blit(mapGrass, (currentPlayer.x, currentPlayer.y))
		currentPlayer.setDirection('R')
	elif keys[pygame.K_UP] and currentPlayer.y > currentPlayer.vel:
		curx = int((currentPlayer.x)/30)
		cury = int((currentPlayer.y-30)/30)
		collisionWith = Collision(curx, cury)
		print(collisionWith)
		if collisionWith != "Brick" and collisionWith != "Metal" and collisionWith != "Water" :
			currentPlayer.y -= currentPlayer.vel
			if collisionWith == "Grass":
				print("Hide under")
				window.blit(mapGrass, (currentPlayer.x, currentPlayer.y))
		currentPlayer.setDirection('U')
	elif keys[pygame.K_DOWN] and currentPlayer.y < (screenHeight - currentPlayer.height - currentPlayer.vel):
		curx = int((currentPlayer.x)/30)
		cury = int((currentPlayer.y+30)/30)
		collisionWith = Collision(curx, cury)
		print(collisionWith)
		if collisionWith != "Brick" and collisionWith != "Metal" and collisionWith != "Water" :
			currentPlayer.y += currentPlayer.vel
			if collisionWith == "Grass":
				print("Hide under")
				window.blit(mapGrass, (currentPlayer.x, currentPlayer.y))
		currentPlayer.setDirection('D')

	redrawGameWindow()

pygame.quit()