# Import the API objects
from api import State, util
from mctspy.tree.nodes import Node
from mctspy.tree.search import MonteCarloTreeSearch
# from .Node import Node
import random
import time

class Bot:
	__root = None

	__max_depth = 8
	__randomize = True

	def __init__(self):
		pass

	def get_move(self, state):
		if state.get_phase() == 1:
			initial_board_state = state.make_assumption()
			root = Node(initial_board_state)
			mcts = MonteCarloTreeSearch(root)
			start_time = time.time()
			best_move = mcts.best_move(5000)
			end_time = time.time()
			print(end_time-start_time)
			return best_move
		else:
			val, move = self.value(state)

			return move

	def value(self, state, alpha=float('-inf'), beta=float('inf'), depth = 0):
		"""
		Return the value of this state and the associated move
		:param State state:
		:param float alpha: The highest score that the maximizing player can guarantee given current knowledge
		:param float beta: The lowest score that the minimizing player can guarantee given current knowledge
		:param int depth: How deep we are in the tree
		:return val, move: the value of the state, and the best move.
		"""
		if state.finished():
			winner, points = state.winner()
			return (points, None) if winner == 1 else (-points, None)

		if depth == self.__max_depth:
			return heuristic(state)

		best_value = float('-inf') if maximizing(state) else float('inf')
		best_move = None

		moves = state.moves()

		if self.__randomize:
			random.shuffle(moves)

		for move in moves:
			next_state = state.next(move)
			value, _ = self.value(next_state, alpha, beta, depth + 1)

			if maximizing(state):
				if value > best_value:
					best_value = value
					best_move = move
					alpha = best_value
			else:
				if value < best_value:
					best_value = value
					best_move = move
					beta = best_value

			# Prune the search tree
			# We know this state will never be chosen, so we stop evaluating its children
			if alpha >= beta:
				break

		return best_value, best_move

def maximizing(state):
	# type: (State) -> bool
	"""
	Whether we're the maximizing player (1) or the minimizing player (2).

	:param state:
	:return:
	"""
	return state.whose_turn() == 1

def heuristic(state):
	# type: (State) -> float
	"""
	Estimate the value of this state: -1.0 is a certain win for player 2, 1.0 is a certain win for player 1

	:param state:
	:return: A heuristic evaluation for the given state (between -1.0 and 1.0)
	"""
	return util.ratio_points(state, 1) * 2.0 - 1.0, None

def ISMCTS(rootstate, itermax, verbose = False):
	""" Conduct an ISMCTS search for itermax iterations starting from rootstate.
		Return the best move from the rootstate.
	"""

	rootnode = Node()
	
	for i in range(itermax):
		node = rootnode
		
		# Determinize
		sample_state = rootstate.make_assumption()
		#sample_state = state.make_assumption()
		
		# Select
		state = sample_state.clone()
		while not state.finished()  and node.GetUntriedMoves(state.moves()) == []: # node is fully expanded and non-terminal
			node = node.UCBSelectChild(state.moves())
			state = state.next(node.move)

		#print("SELECT")

		# Expand
		
		if not state.finished(): # if we can expand (i.e. state/node is non-terminal)
			untriedMoves = node.GetUntriedMoves(state.moves())
			m = random.choice(untriedMoves) 
			player = state.whose_turn()
			state = state.next(m)
			node = node.AddChild(m, player) # add child and descend tree
		
		#print("EXPAND")

		state = sample_state.clone()
		# Simulate
		while not state.finished(): # while state is non-terminal
			state = state.next(random.choice(state.moves()))

		#print("SIMULATE")

		#state = sample_state
		# Backpropagatex
		while node != None: # backpropagate from the expanded node and work back to the root node
			node.Update(state)
			node = node.parentNode
		
		#print("BACKPROP")

	# Output some information about the tree - can be omitted
	if (verbose): 
		print(rootnode.TreeToString(0))
	else: 
		print(rootnode.ChildrenToString())

	return max(rootnode.childNodes, key = lambda c: c.visits + c.avails + c.wins).move