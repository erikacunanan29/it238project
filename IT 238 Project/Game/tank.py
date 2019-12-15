from pygame import image

class Tank(object):
	left = image.load('Images/leftTank.jpg')
	right = image.load('Images/rightTank.jpg')
	up = image.load('Images/upTank.jpg')
	down = image.load('Images/downTank.jpg')
	
	explode = image.load('Images/explode.jpg')
	vanish = image.load('Images/vanish.jpg')

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
		self.state = True

		#Computes the total points garnered by the player
		self.totalPoints = 0


	#Gets the bounding box for collision - left, top, right, bottom
	@property
	def hitbox(self):
		return (self.x, self.y, self.width, self.height)

	def drawObject(self, window):
		if self.enemyHit: #If the tank is hit, render the explode sprite
			#window.blit(explode, (self.x, self.y))
			window.blit(Tank.vanish, (self.x, self.y))
		else: #If the tank is simply moving, render the tank with appropriate direction
			if self.leftSide:
				window.blit(Tank.left, (self.x, self.y))
			elif self.rightSide:
				window.blit(Tank.right, (self.x, self.y))
			elif self.upSide:
				window.blit(Tank.up, (self.x, self.y))
			elif self.downSide:
				window.blit(Tank.down, (self.x, self.y))

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

	def move(self, x_inc, y_inc):
		self.x += x_inc
		self.y += y_inc

	def setPosition(self, x, y):
		self.x = x
		self.y = y

	#Function that resets variables of a tank after it has been hit
	def respawn(self):
		self.enemyHit = False
		self.leftSide = True
		self.state = True 
		window.blit(Tank.left, (self.x, self.y))

