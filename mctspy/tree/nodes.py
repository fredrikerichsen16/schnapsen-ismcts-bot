import numpy as np
from collections import defaultdict
from abc import ABC, abstractmethod
from api import util, State


class MonteCarloTreeSearchNode(ABC):

    def __init__(self, state, move_played=None, parent=None):
        """
        Parameters
        ----------
        state : mctspy.games.common.TwoPlayersAbstractGameState
        parent : MonteCarloTreeSearchNode
        """
        self.state = state
        self.move_played = move_played
        self.parent = parent
        self.children = []

    @property
    @abstractmethod
    def untried_actions(self):
        """

        Returns
        -------
        list of mctspy.games.common.AbstractGameAction

        """
        pass

    @property
    @abstractmethod
    def q(self):
        pass

    @property
    @abstractmethod
    def n(self):
        pass

    @abstractmethod
    def expand(self):
        pass

    @abstractmethod
    def is_terminal_node(self):
        pass

    @abstractmethod
    def rollout(self):
        pass

    @abstractmethod
    def backpropagate(self, reward):
        pass

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):        
        return possible_moves[np.random.randint(len(possible_moves))]


class TwoPlayersGameMonteCarloTreeSearchNode(MonteCarloTreeSearchNode):

    def __init__(self, state, move_played=None, parent=None):
        super().__init__(state, move_played, parent)
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self._untried_actions = None

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.moves()
        return self._untried_actions

    @property
    def q(self):
        wins = self._results[self.parent.state.whose_turn()]
        loses = self._results[util.other(self.parent.state.whose_turn())]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.next(action)
        child_node = TwoPlayersGameMonteCarloTreeSearchNode(next_state, action, self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.finished()

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.finished():
            possible_moves = current_rollout_state.moves()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.next(action)
        #print(util.difference_points(current_rollout_state, current_rollout_state.whose_turn()))
        winner, points = current_rollout_state.winner()
        return 1 if winner == 1 else -1

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)
