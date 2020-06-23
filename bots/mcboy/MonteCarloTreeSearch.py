class MonteCarloTreeSearch:

	def __init__(self, node):
		self.root = node

	def best_move(self, simulations_number):
		"""
		Returns the best move
		:param int simulations_number: how many times we want simulations to be performed
		:return best_move: the best move after performing the simulations
		"""
		for _ in range(0, simulations_number):
			node_selected = self.node_selection() # SELECTION & EXPANSION
			game_result = node_selected.simulate() # SIMULATION
			node_selected.backpropagate(game_result) #BACKPROPAGATION
		# to select the best child we go only for exploitation, so value 0 for exploration parameter
		best_child = self.root.best_child(exploration = 0.)
		best_move = best_child.move_played
		# self.print_brothers_of(best_child)
		return best_move

	def node_selection(self):
		"""
		Selects to node to run the simulation on
		"""
		current_node = self.root
		while not current_node.is_terminal_node:
			if not current_node.is_fully_expanded:
				return current_node.expand() # EXPANSION
			else:
				current_node = current_node.best_child() # EXPLORATION
		return current_node

	def print_brothers_of(self, best_child):
		for child in best_child.parent.children:
			if child == best_child:
				print("------------------------------------------------")
			print(child)
			if child == best_child:
				print("------------------------------------------------")
