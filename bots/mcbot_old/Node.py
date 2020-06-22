import math
import time
from api import util

class Node:

    def __init__(self, state, parent, move, children=[], player=1):
        self.state = state        # Node state
        self.parent = parent      # Parent node
        self.move = move          # Move that got us from parent node to this node
        self.children = children  # Child nodes
        self.player = player      # Player whose turn it is to make a move from this node

        self.wins = 0
        self.visits = 0
        self.avails = 1

    def run(self, state):
        for i in range(20):
            self.init(state)

            for _ in range(250):
                result, leaf = self.explore(self)
                
                leaf.wins += result
                while leaf.parent:
                    leaf = leaf.parent
                    leaf.wins += result

        max_score = -1
        best_move = None
        for child in self.children:
            print(child)
            ratio = child.wins / child.visits
            if ratio > max_score:
                max_score = ratio
                best_move = child.move
        
        return best_move

    def init(self, state):
        self.state = state.clone().make_assumption()
        self.children = []
        self.expand()
        self.visits = 1

    def explore(self, node):
        if node.requires_expansion():
            node.expand()

        newnode = self.select_child(node)

        if(newnode.state.finished() or newnode.state.get_phase() == 2):
            return (self.evaluate(newnode), newnode)

        return self.explore(newnode)
    
    def requires_expansion(self):
        return self.visits == 1 and not self.state.finished() and not self.state.get_phase() == 2
    
    def evaluate(self, node):
        p1_points = node.state.get_points(self.get_me())
        p2_points = node.state.get_points(util.other(self.get_me()))

        return 1 if p1_points - p2_points > 0 else 0

    def select_child(self, node, constant=0.7):
        """
        Use the UCB1 formula to select a child node, filtered by the given list of legal moves.
		exploration is a constant balancing between exploitation and exploration, with default value 0.7 (approximately sqrt(2) / 2)

		"""
        # Get the child with the highest UCB score
        s = max(node.children, key = lambda n: float(n.wins)/float(n.visits) + constant * math.sqrt(math.log(node.visits)/float(n.visits)))

        for child in node.children:
            child.avails += 1

        s.visits += 1

        return s

    def expand(self):
        player = self.state.whose_turn()
        moves = self.state.moves()
        
        for move in moves:
            new_state = self.state.next(move)
            child_node = Node(new_state, self, move, [], util.other(player))
            self.children.append(child_node)

    def get_me(self):
        node = self
        while node.parent:
            node = node.parent
        return node.player

    def __repr__(self):
        return "[M:%s W/V/A: %4i/%4i/%4i]" % (self.move, self.wins, self.visits, self.avails)

            
