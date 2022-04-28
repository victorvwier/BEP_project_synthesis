import copy
import random
from math import sqrt, log
from typing import Union

from common.program import Program
from common.tokens.abstract_tokens import Token, InvalidTransition
from common.tokens.control_tokens import LoopIterationLimitReached
from solver.search.search_algorithm import SearchAlgorithm


class MCTSNode:

    def __init__(self, parent: 'MCTSNode', token: Token, search_algorithm: SearchAlgorithm, state: tuple, visited: set):
        self.parent = parent
        self.token = token
        self.search_algorithm = search_algorithm
        self.state = state
        self.visited = visited

        self.children: list['MCTSNode'] = []
        self.visits: int = 0
        self.total_reward: float = 0
        self.uct = 0

        self.unexplored = [t for t in search_algorithm.tokens]
        self.reward = self.search_algorithm.normalized_reward(self.state)
        self.terminal = None

        if self.reward == self.search_algorithm.best_cost:
            self.best_program = self.rebuild_program()

    @classmethod
    def root(cls, sa: SearchAlgorithm):
        return MCTSNode(None, None, sa, sa.input_state, {sa.input_state})

    @classmethod
    def node(cls, parent: 'MCTSNode', state: tuple, token: Token):
        return MCTSNode(parent, token, parent.search_algorithm, state, parent.visited)

    def calc_uct(self) -> float:
        if self.visits == 0:
            return 0

        exploit = self.total_reward / self.visits
        explore = self.search_algorithm.c_exploration * sqrt(log(self.parent.visits) / self.visits)

        assert -1 <= exploit <= 1
        assert 0 <= explore

        return exploit + explore

    def select(self) -> 'MCTSNode':
        node = self

        while node.reward < 1:
            if len(node.unexplored) > 0 or len(node.children) == 0:
                return node

            node = max(node.children, key=lambda c: c.uct)

        return node

    def expand(self) -> Union['MCTSNode', None]:
        if not self.unexplored:
            if not self.children:
                self.back_propagate(-1)

            return None

        token = self.unexplored.pop(0)

        try:
            new_state = tuple([token.apply(copy.deepcopy(s)) for s in self.state])
        except (InvalidTransition, LoopIterationLimitReached):
            return self.expand()

        if new_state in self.visited:
            return self.expand()

        child = MCTSNode.node(self, new_state, token)
        self.children.append(child)
        self.visited.add(child.state)

        return child

    def rollout(self, max_token_tries: int) -> float:
        state = copy.deepcopy(self.state)

        tokens = []
        for _ in range(max_token_tries):
            token = random.choice(self.search_algorithm.tokens)
            tokens.append(token)

            try:
                state = tuple([token.apply(s) for s in state])
            except (InvalidTransition, LoopIterationLimitReached):
                continue

        reward = self.search_algorithm.normalized_reward(state)

        if reward == 1:
            self.search_algorithm.best_program = Program(self.rebuild_program() + tokens)

        return reward

    def back_propagate(self, reward: float):
        self.visits += 1
        self.total_reward += reward

        if self.parent is not None:
            self.parent.back_propagate(reward)
            self.uct = self.calc_uct()

    def rebuild_program(self) -> list[Token]:
        if self.parent is None:
            return []

        res = self.parent.rebuild_program()
        res.append(self.token)

        return res


class MCTS(SearchAlgorithm):

    def __init__(self, c_exploration: float, rollout_depth: int):
        self.c_exploration = c_exploration
        self.rollout_depth = rollout_depth
        self.root = None

    def setup(self):
        #print(self.c_exploration)
        self.root = MCTSNode.root(self)

    def iteration(self):
        selected_node = self.root.select()
        #print("Selected {}".format(selected_node.state))
        program = selected_node.rebuild_program()

        if selected_node.reward == 1:
            self.best_program = Program(selected_node.rebuild_program())
            return False

        new_node = selected_node.expand()
        #print("Expanded {}".format(new_node.state)) if new_node is not None else print("Expanded {}".format(new_node))

        if new_node is None:
            return True

        if new_node.reward == 1:
            self.best_program = Program(new_node.rebuild_program())
            return False

        reward = new_node.rollout(self.rollout_depth) if new_node is not None else 0
        #print("Rollout {}".format(reward))

        if reward == 1:
            return False

        new_node.back_propagate(reward) if new_node is not None else selected_node.back_propagate(reward)
        #print("Back propagated")

        return True

