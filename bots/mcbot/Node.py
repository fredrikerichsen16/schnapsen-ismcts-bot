import math
from api import util

class Node:

    def __init__(self, state, parent, move, children=[], player=1):
        self.state = state.clone(player) # State of current node
        self.parent = parent             # Parent node
        self.move = move                 # Move that got us from parent node to this node
        self.children = children         # Child nodes
        self.player = player             # Player whose turn it is to make a move from this node

        self.wins = 1
        self.visits = 1
        self.avails = 1

    def run(self):
        for _ in range(1000):
            result, leaf = self.explore(self)
            
            leaf.wins += result
            while leaf.parent:
                leaf = leaf.parent
                leaf.wins += result

        max_score = -1
        best_move = None
        print(len(self.children))
        for child in self.children:
            ratio = child.wins / child.visits
            if ratio > max_score:
                max_score = ratio
                best_move = child.move
        
        return best_move


    def explore(self, node):
        if not node.children:
            node.expand()

        newnode = self.select_child(node)

        if(newnode.state.finished() or newnode.state.get_phase() == 2):
            return (self.evaluate(newnode), newnode)

        return self.explore(newnode)
    
    def evaluate(self, node):
        p1_points = node.state.get_points(1)
        p2_points = node.state.get_points(2)

        return 1 if p1_points - p2_points > 0 else 0

    def select_child(self, node, constant=0.7):
        """
        Use the UCB1 formula to select a child node, filtered by the given list of legal moves.
		exploration is a constant balancing between exploitation and exploration, with default value 0.7 (approximately sqrt(2) / 2)

		"""
        # Get the child with the highest UCB score
        s = max(node.children, key = lambda n: float(n.wins)/float(n.visits) + constant * math.sqrt(math.log(n.avails)/float(n.visits)))

        for child in node.children:
            child.avails += 1

        s.visits += 1

        return s

    def expand(self):
        st = self.state

        player = st.whose_turn()
        player = util.other(player)

        if player == 1:
            st = self.state.make_assumption()
        
        moves = st.moves()
        
        for move in moves:
            new_state = st.next(move)
            child_node = Node(new_state, self, move, [], player)
            self.children.append(child_node)

            
