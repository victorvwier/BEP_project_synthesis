from collections import deque
from typing import List, Union

from anytree import NodeMixin

from common.tokens.abstract_tokens import TransToken, EnvToken, BoolToken, InventedToken

from common.prorgam import Program
from search.MCTS.exceptions import InvalidRewardValue

# MAX_PROGRAM_DEPTH = 200
# MAX_SIMULATION_DEPTH = 3
# TODO check if loop_limit is given along with functions everywhere where possible
LOOP_LIMIT = 100


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
            env_tokens: deque[EnvToken],
            loss: float,
    ):

        return SearchTreeNode(
            # program=Program([]),
            chosen_token=None,
            unexplored_succeeding_tokens=env_tokens,
            loss=loss
        )
