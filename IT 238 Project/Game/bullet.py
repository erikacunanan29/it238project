from pygame import image

class Bullet(object):
	downBullet = image.load('Images/downBullet.png')
	leftBullet = image.load('Images/leftBullet.png')
	rightBullet = image.load('Images/rightBullet.png')
	upBullet = image.load('Images/upBullet.png')

	def __init__(self, x, y, facing, player):
		self.x = x
		self.y = y
		self.player = player
		self.facing = facing
		self.vel = 15


	#Function that renders the bullet depending on the direction the tank is facing
	def drawObject(self, window):
		if self.facing == 'L':
			window.blit(Bullet.leftBullet, (self.x, self.y-10))
		elif self.facing == 'R':
			window.blit(Bullet.rightBullet, (self.x, self.y-10))
		elif self.facing == 'U':
			window.blit(Bullet.upBullet, (self.x-10, self.y))
		elif self.facing == 'D':
			window.blit(Bullet.downBullet, (self.x-10, self.y))
