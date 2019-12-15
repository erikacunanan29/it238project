import socket as _s
from random import randint, seed
import string
import select
import threading


from Net.packet import *
from Game.game import *
from Game.tank import *
from config import *

def getSocketId(s):
  try:
    return '{}:{}'.format(s.getsockname()[0], s.getsockname()[1])
  except AttributeError:
    return '{}:{}'.format(s[0], s[1])

def generateRandomId(typeof='', size=4, chars=string.ascii_uppercase + string.digits):
  '''
  params:
    typeof = for added security (think of `salt`)
    size = length of id
    chars = characters to use in id
  '''
  return typeof[0] + ''.join(random.choice(chars) for _ in range(size))


class Peer():
	def __init__(self, game):
		self.game = game
		self.socket = _s.socket(_s.AF_INET, _s.SOCK_DGRAM)
		self.socket.setsockopt(_s.SOL_SOCKET, _s.SO_BROADCAST, 1)
		self.peer_list = dict()
		self.confirm_list = dict()
		self.is_connected = False
		self.thread = threading.Thread(target=self.listen)
		self.ready_count = 0


	def start(self):
		self.thread.start()

	def listen(self):
		if self.is_connected:
			return

		self.socket.bind((HOST, 0))

		self.is_connected = True
		print('you are now listening at', getSocketId(self.socket))
		while self.is_connected:
			rsockets, wsockets, esockets = select.select([self.socket], [], [])

			for s in rsockets:
				if s == self.socket:
					data, addr = s.recvfrom(1024)
					self.handleReceive(data, addr)


	def broadcast(self, data):
		if data:
			for p in self.peer_list:
				self.socket.sendto(data, p)
	
	def handleReceive(self, data, sender):
		if data:
			print('\treceived data: {} from {}'.format(str(data), getSocketId(sender)))
			data = data.decode('utf-8')
			data = PacketBuilder.unpack(data)
			packet_type = data[0]
			data = data[1:]

			if PacketType(packet_type) == PacketType.CONNECT:
				# reply with map
				# broadcast join
				# reply 'JOIN'
				# add to peer list

				print('\tsending map...')
				packet = PacketBuilder.pack(PacketType.MAP, [self.game.mapName])
				self.socket.sendto(packet, sender)

				print('\tbroadcasting', sender, '...')
				packet = PacketBuilder.pack(PacketType.JOIN, [data[0], sender[0], str(sender[1])])
				self.broadcast(packet)

				for s in self.peer_list.keys():
					print('\tintroducing {} to {}...'.format(self.peer_list[s], data[0]))
					packet = PacketBuilder.pack(PacketType.JOIN, [self.peer_list[s], s[0], str(s[1])])
					self.socket.sendto(packet, sender)

				self.peer_list[sender] = data[0]

			elif PacketType(packet_type) == PacketType.DISCONNECT:
				pass

			elif PacketType(packet_type) == PacketType.JOIN:
				print('{} has joined!'.format(data[0]))
				sock = (data[1], int(data[2]))
				self.peer_list[sock] = data[0]

			elif PacketType(packet_type) == PacketType.MAP:
				self.game.mapName = data[0]

			elif PacketType(packet_type) == PacketType.READY:
				self.peer_list[sender] = data[2] if self.peer_list[sender] == '' else self.peer_list[sender]

				print(self.peer_list)
				x = int(data[0])
				y = int(data[1])
				self.game.appendPlayer( Tank(self.peer_list[sender], x, y) )

				self.ready_count += 1

			elif PacketType(packet_type) == PacketType.MOVE:
				self.game.players[data[0]].setPosition( int(data[1]), int(data[2]) )
				self.game.players[data[0]].setDirection(data[3])

			elif PacketType(packet_type) == PacketType.BULLET_DRW:
				name = data[0]
				x = int(data[1])
				y = int(data[2])
				facing = data[3]
				self.game.drawBullet(x, y, facing, name)

			elif PacketType(packet_type) == PacketType.TANK_RMV:
				name = data[0]
				self.game.players[name].state = False

			elif PacketType(packet_type) == PacketType.SCORE_UPDT:
				name = data[0]
				self.game.players[name].totalPoints += 100

			elif PacketType(packet_type) == PacketType.GAMESTATE:
				self.game.state = State[data[0]]

	def connect(self, server):
		packet = PacketBuilder.pack(PacketType.CONNECT, [self.game.name])
		self.peer_list[server] = ''
		self.socket.sendto(packet, server)

	def disconnect(self):
		pass

	def updateGameState(self, state):
		packet = PacketBuilder.pack(PacketType.GAMESTATE, [state])
		self.broadcast(packet)
		self.game.state = State[state]

	def ready(self):
		packet = PacketBuilder.pack(PacketType.READY, [str(self.game.me.x), str(self.game.me.y), self.game.name])
		self.broadcast(packet)
