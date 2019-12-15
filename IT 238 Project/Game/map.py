from pygame import image

class Map(object): #Supposed to be for setting up the map but the map template is still missing
	brick = image.load('Images/map_Brick.jpg')
	steel = image.load('Images/map_Steel.jpg')
	grass = image.load('Images/map_Grass.jpg')
	water = image.load('Images/map_Water.jpg')

	def __init__(self, x, y, element):
		self.x = x
		self.y = y
		self.element = element
		self.state = [] #Can be crossed, can be broken, can bullets pass through
		self.hitbox = (self.x, self.y, 30, 28) # sets bounding box for the map


	def drawObject(self, window):
		if self.element == '#': #bricks #
			window.blit(Map.brick, (self.x, self.y))
			self.state = [False, True, False]
		elif self.element == '@': #steel walls @
			window.blit(Map.steel, (self.x, self.y))
			self.state = [False, False, False]
		elif self.element == '%': #bush %
			window.blit(Map.grass, (self.x, self.y))
			self.state = [True, False, True]
		elif self.element == '~': #water ~
			window.blit(Map.water, (self.x, self.y))
			self.state = [False, False, True]
