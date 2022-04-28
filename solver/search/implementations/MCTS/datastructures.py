import math
from collections import deque
from typing import Union

from anytree import NodeMixin

from common.tokens.abstract_tokens import InventedToken
from solver.search.implementations.MCTS.exceptions import InvalidRewardValue


class TokenScore:
    def __init__(self, score: int, visits: int, max_token_try: int):
        """Keeps track of score of a token. Score will be set to -inf"""
        self._score = score
        self._visits = visits
        self._max_token_try = max_token_try

    @property
    def visits(self):
        return self._visits

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, new_score):

        # checks if score was not set to a (negative) infinity earlier.
        assert(not math.isinf(self.score))

        if self.visits >= (self._max_token_try-1):
            pass

        # if this is the fifth time the score is updated and it was -1 every time, set score to infinity
        if new_score == -self._max_token_try and self.visits == (self._max_token_try-1):
            if self.score == (-self._visits):
                self._score = float("-inf")
                self._visits += 1
                return

        self._score = new_score
        self._visits += 1

    def __repr__(self):
        return "TokenScore(score: %s, visits: %s)" % (self.score, self.visits)


class SearchTreeNode(NodeMixin):
    def __init__(
            self,
            # program: Program,
            chosen_token: Union[InventedToken, None],
            unexplored_succeeding_tokens: deque[InventedToken],
            loss: float,
            number_of_visits: int = 0,
            total_obtained_reward: float = 0.0,       # should be between 0 and 1
            greatest_obtained_reward: float = 0.0,    # should be between 0 and 1
            parent=None,
            children=None
    ):
        # self.program = program
        self.chosen_token = chosen_token
        self.unexplored_succeeding_tokens = unexplored_succeeding_tokens
        self.loss = loss
        self.number_of_visits = number_of_visits
        self._total_obtained_reward = total_obtained_reward
        self._greatest_obtained_reward = greatest_obtained_reward
        self.parent = parent
        if children:
            self.children = children

    @property
    def total_obtained_reward(self):
        """A reward is expected to be between 0 and 1. Rewards are computed with the following formula:
        (max_expected_loss - obtained_loss) / max_expected_loss"""
        return self._total_obtained_reward

    @total_obtained_reward.setter
    def total_obtained_reward(self, new_total_reward):
        self._total_obtained_reward = new_total_reward

    @property
    def greatest_obtained_reward(self):
        """Is expected to be between 0 and 1. Rewards are computed with the following formula:
        (max_expected_loss - obtained_loss) / max_expected_loss"""
        return self._greatest_obtained_reward

    @greatest_obtained_reward.setter
    def greatest_obtained_reward(self, reward):
        if reward > 1.001:
            raise InvalidRewardValue("Reward should be smaller than 1.001")

        self._greatest_obtained_reward = reward

    def __repr__(self):
        return "SearchTreeNode(Token: %s, visits: %s, height: %s)" \
               % (self.chosen_token, self.number_of_visits, self.height)

    @staticmethod
    def initialize_search_tree(
            env_tokens: deque[InventedToken],
            loss: float,
    ):

        return SearchTreeNode(
            # program=Program([]),
            chosen_token=None,
            unexplored_succeeding_tokens=env_tokens,
            loss=loss
        )
