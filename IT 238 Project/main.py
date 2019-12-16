import pygame
import threading
import random
import sys
from threading import Timer

from Game.tank import *
from Game.bullet import *
from Game.map import *
from Game.game import *
from Net.peer import *


class Game(object):
	def __init__(self, name):
		self.state = State.LOBBY
		self.name = name
		self.mapName = ''
		self.me = Tank(name, 0, 0)
		self.players = dict()
		self.bullets = []

	def loadMap(self, map_num):
		self.mapName = 'Maps/map{}.txt'.format( str(map_num) )

	def initMap(self, mapElements, mapData):
		i = 0
		j = 0

		with open(self.mapName, 'r') as f:
			for line in f:
				mapData.append(line)
				j = 0
				for c in line:
					mapElements.append(Map(j, i, c))
					j += 30
				i += 30

		while True:
			x = random.randint(0,21)
			y = random.randint(0,33)
			if mapData[x][y] == '.':
				self.me.setPosition(y*30, x*30)
				self.appendPlayer(self.me)
				break

		return True

	def getPlayerObjects(self):
		return list(self.players.values())

	def initPlayerPos(self):
		pass

	def appendPlayer(self, tank):
		self.players[tank.nickname] = tank
		pass

	def drawBullet(self, x, y, facing, shooter):
		self.bullets.append(Bullet(x, y, facing, shooter))
		pass

	def removeBullet(self):
		pass

	def removeElement(self):
		pass
		# removes map element upon hitting


#---------------------------------- MAIN FUNCTIONALITY ---------------------------------- #

#Renders the tally of the scores of the players
def highscores():
	pygame.draw.rect(window, (167, 158, 159), (1000, 0, 250, 700))
	startY = 75

	font = pygame.font.SysFont("Trebuchet MS", 30, True)

	text = font.render("SCOREBOARD", 1, (0, 0, 0))
	window.blit(text, (1035, 25))

	for player in game.getPlayerObjects():
		name = font.render(player.nickname, 1, (0, 0, 0))
		score = font.render(str(player.totalPoints), 1, (0, 0, 0))

		window.blit(name, (1040, startY))
		window.blit(score, (1155, startY))


		startY += 45

#Re-draws the window to display the updates of the game
def redrawGameWindow():
	window.fill((0, 0, 0))

	highscores()

	for player in game.getPlayerObjects():
		if player.state:
			player.drawObject(window)
		#commented out respawn to test game over
		if player.enemyHit:
			t = Timer(5, player.respawn)
			t.start()


	for bullet in game.bullets:
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


init_map = False
mapElements = []
mapData = []

try:
	name = sys.argv[1]
	game = Game(name)
	peer = Peer(game)
	peer.start()
	
	addr = sys.argv[2]
	port = sys.argv[3]
	print('welcome {}. connecting to {}:{}'.format(name, addr, port))
	peer.connect((addr, int(port)))

except IndexError as e:
	if len(sys.argv) != 2:
		print('-----------------------------------------')
		print('number of args is invalid. the following are valid commands:')
		print('"python3 main.py <name>" - creates a game lobby where peers can connect')
		print('"python3 main.py <name> <server_addr> <server_port>" - a peer connects to the given lobby')
		print('\tanyone can connect to a peer as long as it is also connected to a lobby')
		print('\tanyone can freely quit as soon as the game starts')
		sys.exit(2)

	print('no server inputted, creating server.. ')
	# init map
	cmd=''
	init_map = True
	game.loadMap( random.randint(1,3) )
	game.initMap(mapElements, mapData)


while not init_map:
	if game.mapName != '':
		game.initMap(mapElements, mapData)
		init_map = True

cmd = ''
while cmd != 'ready':
	cmd = input('enter ready to start game: ')

peer.ready()
peer.ready_count += 1


while peer.ready_count != len(peer.peer_list)+1:
	pass

print('GAME TIME!')

pygame.init()

screenWidth = 1000
screenHeight = 700

window = pygame.display.set_mode((screenWidth+250, screenHeight))
pygame.display.set_caption("Battle City - {}".format(game.name))


run = True
while run:
	pygame.time.delay(50)

	#Checks if the user has exitted the program
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	#For every bullet that is shot in the game
	for bullet in game.bullets:

		player = game.me
		if player.nickname != bullet.player: #Checks if the bullet has hit a player
			if bullet.y < player.hitbox[1] + player.hitbox[3] and bullet.y > player.hitbox[1]:
				if bullet.x > player.hitbox[0] and bullet.x < player.hitbox[0] + player.hitbox[2]:
					print('you are hit by {}'.format(bullet.player))

					# remove your tank from other players
					packet = PacketBuilder.pack(PacketType.TANK_RMV, [game.name])
					peer.broadcast(packet)
					# update the score of the one that hit a tank
					packet = PacketBuilder.pack(PacketType.SCORE_UPDT, [bullet.player])
					peer.broadcast(packet)

					game.bullets.pop(game.bullets.index(bullet))
					player.state = False
					game.players[bullet.player].totalPoints += 100
					#game.me.totalPoints += 100 #The attacker will get points for defeating the enemy
					#player.enemyHit = True #Tells the attacked tank that it has been defeated
					#player.state = False #set the state of the Player to inactive since it has been hit
					#print('player removed')


		#Checks if bullet hit an element
		for i in range(0, len(mapElements)):
			if mapElements[i].element == '#':
				if bullet.y < mapElements[i].hitbox[1] + mapElements[i].hitbox[3] and bullet.y > mapElements[i].hitbox[1]:
					if bullet.x > mapElements[i].hitbox[0] and bullet.x < mapElements[i].hitbox[0] + mapElements[i].hitbox[2]:
						game.bullets.pop(game.bullets.index(bullet))
						#mapElements[i].element = '.'
						mapElements.pop(i)
						print("bullet hit a brick")
						break
			elif mapElements[i].element == '@':
				if bullet.y < mapElements[i].hitbox[1] + mapElements[i].hitbox[3] and bullet.y > mapElements[i].hitbox[1]:
					if bullet.x > mapElements[i].hitbox[0] and bullet.x < mapElements[i].hitbox[0] + mapElements[i].hitbox[2]:
						game.bullets.pop(game.bullets.index(bullet))
						# mapElements[i].element = '.'
						print("bullet hit steel")
			else:
				continue


		#Checks if the bullet has exceeded the minimum maximum boundaries of the screen
		if bullet.x < screenWidth-30 and bullet.facing == 'R' and bullet.x > 0:
			bullet.x += bullet.vel

		elif bullet.x > 0 and bullet.facing == 'L':
			bullet.x -= bullet.vel
		elif bullet.y < screenHeight and bullet.facing == 'D' and bullet.y > 0:
			bullet.y += bullet.vel
		elif bullet.y > 0 and bullet.facing == "U":
			bullet.y -= bullet.vel
		else:
			game.bullets.pop(game.bullets.index(bullet))

	k = 0
	winner ={}
	#get active players
	for player in game.getPlayerObjects():
		if player.state == True:
			k = k+1
			winner.update({player.nickname:player.totalPoints})
	#if there is only one active player he/she is the winner, game ends
	if k == 1:
		#print(winner)
		champion = list(winner.keys())
		print(champion)
		run = False
		show_game_over(champion[0])


	keys = pygame.key.get_pressed() #Determines which keys are pressed

	#If the player has shot a bullet
	if game.me.state and keys[pygame.K_SPACE] and (game.me.firedBullet == False or len(game.bullets) == 0):
		if game.me.leftSide:
			facing = 'L'
		elif game.me.rightSide:
			facing = 'R'
		elif game.me.upSide:
			facing = 'U'
		elif game.me.downSide:
			facing = 'D'

		if (len(game.bullets) < 1):
			x = round(game.me.x+game.me.height//2)
			y = round(game.me.y+game.me.width//2)
			game.drawBullet(x, y, facing, game.name)
			game.me.firedBullet = True
			packet = PacketBuilder.pack(PacketType.BULLET_DRW, [game.name, str(x), str(y), facing])
			peer.broadcast(packet)

	#If the player has moved to either up, down, left, right
	if game.me.state and keys[pygame.K_a] or keys[pygame.K_LEFT] and game.me.x > game.me.vel:
		curx = int((game.me.x-30)/30)
		cury = int((game.me.y)/30)
		collisionWith = Collision(curx, cury)
		print(collisionWith)
		if collisionWith != "Brick" and collisionWith != "Metal" and collisionWith != "Water" :
			game.me.x -= game.me.vel
			if collisionWith == "Grass":
				print("Hide under")
				window.blit(Map.grass, (game.me.x, game.me.y))
		game.me.setDirection('L')
		packet = PacketBuilder.pack(PacketType.MOVE, [game.name, str(game.me.x), str(game.me.y), 'L'])
		peer.broadcast(packet)
	elif game.me.state and keys[pygame.K_d] or keys[pygame.K_RIGHT] and game.me.x < (screenWidth - game.me.width - game.me.vel):
		curx = int((game.me.x+30)/30)
		cury = int((game.me.y)/30)
		collisionWith = Collision(curx, cury)
		print(collisionWith)
		if collisionWith != "Brick" and collisionWith != "Metal" and collisionWith != "Water" :
			game.me.x += game.me.vel
			if collisionWith == "Grass":
				print("Hide under")
				window.blit(Map.grass, (game.me.x, game.me.y))
		game.me.setDirection('R')
		packet = PacketBuilder.pack(PacketType.MOVE, [game.name, str(game.me.x), str(game.me.y), 'R'])
		peer.broadcast(packet)
	elif game.me.state and keys[pygame.K_w] or keys[pygame.K_UP] and game.me.y > game.me.vel:
		curx = int((game.me.x)/30)
		cury = int((game.me.y-30)/30)
		collisionWith = Collision(curx, cury)
		print(collisionWith)
		if collisionWith != "Brick" and collisionWith != "Metal" and collisionWith != "Water" :
			game.me.y -= game.me.vel
			if collisionWith == "Grass":
				print("Hide under")
				window.blit(Map.grass, (game.me.x, game.me.y))
		game.me.setDirection('U')
		packet = PacketBuilder.pack(PacketType.MOVE, [game.name, str(game.me.x), str(game.me.y), 'U'])
		peer.broadcast(packet)
	elif game.me.state and keys[pygame.K_s] or keys[pygame.K_DOWN] and game.me.y < (screenHeight - game.me.height - game.me.vel):
		curx = int((game.me.x)/30)
		cury = int((game.me.y+30)/30)
		collisionWith = Collision(curx, cury)
		print(collisionWith)
		if collisionWith != "Brick" and collisionWith != "Metal" and collisionWith != "Water" :
			game.me.y += game.me.vel
			if collisionWith == "Grass":
				print("Hide under")
				window.blit(Map.grass, (game.me.x, game.me.y))
		game.me.setDirection('D')
		packet = PacketBuilder.pack(PacketType.MOVE, [game.name, str(game.me.x), str(game.me.y), 'D'])
		peer.broadcast(packet)

	redrawGameWindow()

pygame.quit()
