import numpy as np
from math import *
import random
from collections import defaultdict
from api import util
class Node():

    def __init__(self, state, move_played=None, parent=None):
        self.state = state
        self.move_played = move_played
        self.parent = parent
        self.children = []
        self.number_of_visits = 0.
        self.outcome = defaultdict(int)
        self.untried_moves = None

    @property
    def get_untried_moves(self):
        if self.untried_moves is None:
            self.untried_moves = self.state.moves()
        return self.untried_moves

    @property
    def q(self):
        wins = self.outcome[self.parent.state.whose_turn()]
        loses = self.outcome[util.other(self.parent.state.whose_turn())]
        return wins - loses

    @property
    def n(self):
        return self.number_of_visits

    def expand(self):
        move = self.untried_moves.pop()
        next_state = self.state.next(move)
        child_node = Node(next_state, move, self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.finished()
    
    def is_fully_expanded(self):
        return len(self.get_untried_moves) == 0

    def simulation_policy(self, possible_moves):        
        return random.choice(possible_moves)

    def simulate(self):
        current_simulation_state = self.state
        while not current_simulation_state.finished():
            possible_moves = current_simulation_state.moves()
            move = self.simulation_policy(possible_moves)
            current_simulation_state = current_simulation_state.next(move)
        winner, points = current_simulation_state.winner()
        return 1 if winner == 1 else -1

    def backpropagate(self, result):
        self.number_of_visits += 1.
        self.outcome[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def best_child(self, exploration=1.4):
        choices_weights = [
            (c.q / c.n) + exploration * sqrt((2 * log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def __repr__(self):
        return "M:{:s}; W:{:.2f}; L:{:.2f}; V:{:.2f}".format(str(self.move_played), self.outcome[1], self.outcome[-1], self.number_of_visits)