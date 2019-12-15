from enum import Enum


class PacketType(Enum):
	SEPARATOR   = '|'
	
	GAMESTATE = 'G'
	CONNECT = '+'
	JOIN = 'J'
	PLAYER_LIST = 'L'
	DISCONNECT = '-'
	
	MAP = 'M'
	READY = 'R'
	
	MOVE = 'V'
	BULLET_DRW = 'B'
	TANK_RMV = 't'
	ELEMENT_RMV = 'e'
	
	SCORE_UPDT = 'U'

class PacketBuilder():
	@staticmethod
	def pack(typeof, data=[]):
		data = [typeof.value] + data
		return PacketType.SEPARATOR.value.join(data).encode('utf-8')

	@staticmethod
	def unpack(packet):
		try:
			packet = packet.decode('utf-8')
		except AttributeError:
			pass
		finally:
			return packet.split(PacketType.SEPARATOR.value)
