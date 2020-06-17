import math

class Node:

    def __init__(self, state, parent, children, move, player):
        self.state = state       # State of current node
        self.parent = parent     # Parent node
        self.children = children # Child nodes
        self.move = move         # Move that got us from parent node to this node
        self.player = player     # Player whose turn it is to make a move from this node

        self.wins = 0
        self.visits = 0
        self.avails = 1

    def run(self):
        for i in range(50):
            self.state = self.state.make_assumption()
            
            for _ in range(1000):
                self.explore(self)

    def explore(self, node):
        if not node.children:
            node.expand()

        newnode = self.select_child(node)

        if(newnode.get_phase() == 2):
            return self.evaluate(newnode)

        self.wins += self.explore(newnode)
    
    def evaluate(self, node):
        p1_points = node.state.get_pending_points(1)
        p2_points = node.state.get_pending_points(2)

        return p1 - p2 > 0

    def select_child(self, node, exploration = 0.7):
		""" Use the UCB1 formula to select a child node, filtered by the given list of legal moves.
			exploration is a constant balancing between exploitation and exploration, with default value 0.7 (approximately sqrt(2) / 2)
		"""

        # Get the child with the highest UCB score
        s = max(node.children, key = lambda n: float(n.wins)/float(n.visits) + 0.7 * sqrt(log(n.avails)/float(n.visits)))

        for child in node.children:
            child.avails += 1

        return s

    def expand(self):
        moves = self.state.moves()
        player = 1 - player # Flip 1 to 0 or vice versa
        
        for move in moves:
            new_state = self.state.next(move)
            child_node = Node(new_state, self, None, move, player)
            self.children.append(child_node)
            
