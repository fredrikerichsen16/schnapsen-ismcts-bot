# Import the API objects
from api import State, util
from .Node import Node
import random

class Bot:

	# How many samples to take per move
	__num_samples = -1
	# How deep to sample
	__depth = -1

	__root = None

	def __init__(self, num_samples=4, depth=8):
		self.__num_samples = num_samples
		self.__depth = depth

	def get_move(self, state):
		if state.get_phase() == 1 and state.whose_turn() == 1:
			self.__root = Node(state, None, None, None, 1)
			self.__root.run()
		else:
			pass