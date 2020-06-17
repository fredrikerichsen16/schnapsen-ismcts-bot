# Import the API objects
from api import State, util
from Node import Node
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

		# Sometimes many moves have the same, highest score, and we'd like the bot to pick a random one.
		# Shuffling the list of moves ensures that.
		random.shuffle(moves)

		best_score = float("-inf")
		best_move = None

		scores = [0.0] * len(moves)

		for move in moves:
			for s in range(self.__num_samples):

				# If we are in an imperfect information state, make an assumption.

				sample_state = state.make_assumption() if state.get_phase() == 1 else state

				score = self.evaluate(sample_state.next(move), player)

				if score > best_score:
					best_score = score
					best_move = move

		return best_move # Return the best scoring move

	def evaluate(self,
				 state,     # type: State
				 player     # type: int
			):
		# type: () -> float
		"""
		Evaluates the value of the given state for the given player
		:param state: The state to evaluate
		:param player: The player for whom to evaluate this state (1 or 2)
		:return: A float representing the value of this state for the given player. The higher the value, the better the
			state is for the player.
		"""

		score = 0.0

		for _ in range(self.__num_samples):
			st = state.clone()

			# Do some random moves
			for i in range(self.__depth):
				if st.finished():
					break

				st = st.next(random.choice(st.moves()))

			score += self.heuristic(st, player)

		return score/float(self.__num_samples)

	def heuristic(self, state, player):
		return util.ratio_points(state, player)