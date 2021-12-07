# import copy
import math
# import random
from collections import deque
from typing import List, Union, Type, Tuple, Dict

from anytree import RenderTree

from common.environment import StringEnvironment, RobotEnvironment, PixelEnvironment, Environment
from common.experiment import Example
from common.prorgam import Program
from common.tokens.abstract_tokens import TransToken, BoolToken, InvalidTransition, InventedToken
from common.tokens.control_tokens import RecursiveCallLimitReached, LoopIterationLimitReached, If, LoopWhile

from search.MCTS.datastructures import SearchTreeNode
from search.MCTS.exceptions import MaxNumberOfIterationsExceededException, InvalidProgramException, \
    SimilarProgramAlreadyFoundException
from search.abstract_search import SearchAlgorithm

# TODO do something with max program depth. This should happen throughout all the code.
# MAX_PROGRAM_DEPTH = 200
# MAX_SIMULATION_DEPTH = 3
from search.search_result import SearchResult

LOOP_LIMIT = 100
EXPLORATION_CONSTANT = 1.0 / math.sqrt(2)
MAX_TOKEN_DEPTH = 3


def deepcopy_program(program: Program) -> Program:
    return Program(
        tokens=[token for token in program.sequence],
        recurse_limit=program.recursive_call_limit,
        loop_limit=program.loop_limit,
    )


class TokenScore():
    def __init__(self, score: int = 0, visits: int = 0):
        self.score = score
        self.visits = visits

    def __repr__(self):
        return "TokenScore(score: %s, visits: %s)" % (self.score, self.visits)

class MCTS(SearchAlgorithm):

    def __init__(self, time_limit_sec: float):
        super().__init__(time_limit_sec)
        self._best_program: Program
        self.smallest_loss: float = float("inf")
        self.max_expected_loss: float = float("inf")  # is used for normalizing exploitation factor
        self.search_tree: Union[SearchTreeNode, None] = None
        self.invented_tokens = List[InventedToken]
        self.input_envs: Tuple[Environment]
        self.output_envs: Tuple[Environment]
        self.dict_with_obtained_output_environments: Dict[Tuple[Environment], SearchTreeNode] = {}
        self.token_scores_dict: Dict[InventedToken, TokenScore] = {}

    # TODO make sure that the type of trans_ and bool_token is set[Type[Token]] and not set[Token]
    def setup(self, training_examples: List[Example], trans_tokens: set[Type[TransToken]],
              bool_tokens: set[Type[BoolToken]]):

        # retrieve input and output environments
        self.input_envs: Tuple[Environment] = tuple(example.input_environment for example in training_examples)
        self.output_envs: Tuple[Environment] = tuple(example.output_environment for example in training_examples)

        # set the best program to be an empty token list and calculate the associated loss
        self._best_program = Program([])
        resulting_envs = MCTS.get_resulting_envs(program=self._best_program, input_envs=self.input_envs)
        self.smallest_loss = MCTS.compute_loss(resulting_envs, self.output_envs)

        # set the max_expected_loss, which will be used to normalize the exploitation factor in the UCT
        self.max_expected_loss = self.smallest_loss

        # compute invented tokens that are composed of several other tokens
        self.invented_tokens: List[InventedToken] = MCTS.MCTS_invent(trans_tokens=trans_tokens, bool_tokens=bool_tokens)
        # add each token to the dictionary with score 0
        for token in self.invented_tokens:
            self.token_scores_dict[token] = TokenScore(score=0, visits=0)

        # initialize the root of the search tree
        self.search_tree: SearchTreeNode = \
            SearchTreeNode.initialize_search_tree(env_tokens=deque(self.invented_tokens), loss=self.smallest_loss)

        # initialize a dictionary that keeps track of outcomes of programs
        self.dict_with_obtained_output_environments[resulting_envs] = self.search_tree

    # TODO make sure that the type of trans_ and bool_token is set[Type[Token]] and not set[Token]
    def iteration(self, training_example: List[Example], trans_tokens: set[Type[TransToken]],
                  bool_tokens: set[Type[BoolToken]]) -> bool:

        # return False to indicate no other iterations are necessary
        if self.smallest_loss <= 0.0001:
            return False

        # TODO implement the following subprocesses
        (selected_node, program) = self.select(self.search_tree, Program([]))
        new_node = self.expand(
            node=selected_node,
            program=program,
        )
        try:
            reward = self.simulate_and_return_reward(
                node=new_node,
                program=program,
            )
            self.back_propagate(new_node, reward)
        except (InvalidProgramException, SimilarProgramAlreadyFoundException):
            # TODO possibly have different strategy for when a similar program was already found
            MCTS.remove_nodes_with_no_possible_extensions(new_node)

        # return True to indicate that another iteration is required
        return True

    def extend_result(self, search_result: SearchResult):
        search_result.dictionary["search_tree"] = self.search_tree

        tree_string = ""
        for pre, fill, node in RenderTree(self.search_tree):
            tree_string += "%s%s \n" % (pre, str(node))
        search_result.dictionary["rendered_tree"] = tree_string

        return search_result

    @staticmethod
    def MCTS_invent(trans_tokens: set[Type[TransToken]], bool_tokens: set[Type[BoolToken]]) -> List[InventedToken]:
        """Returns a list of tokens invented using the given tokens.
        The invented tokens will be:
            - just a single token for each given trans_token
            - an if and while token for each combination of bool_token and trans_token
            - an if and while token for each combination of bool_token and combo of two different_trans_tokens
        """
        invented_tokens: List[InventedToken] = []
        for token_type in trans_tokens:
            invented_tokens.append(InventedToken([token_type()]))

        for bool_token in bool_tokens:
            for trans_token_1 in trans_tokens:
                invented_tokens.append(InventedToken([If(bool_token(), [trans_token_1()], [])]))
                invented_tokens.append(InventedToken([LoopWhile(bool_token(), [trans_token_1()])]))

        for bool_token in bool_tokens:
            for trans_token_1 in trans_tokens:
                for trans_token_2 in trans_tokens:
                    if trans_token_1 != trans_token_2:
                        invented_tokens.append(InventedToken([
                            If(bool_token(), [trans_token_1(), trans_token_2()], [])
                        ]))
                        invented_tokens.append(InventedToken([
                            LoopWhile(bool_token(), [trans_token_1(), trans_token_2()])
                        ]))

        return invented_tokens

    @staticmethod
    def get_resulting_envs(program: Program, input_envs: Tuple[Environment]):
        return tuple(map(lambda env: program.interp(env), input_envs))

    @staticmethod
    def compute_loss_of_program(program: Program, examples: List[Example]) -> float:
        """Gets the average loss function of applying the program to each example.
        Returns float number equal to infinity if one of the examples could not be interpreted with the program"""

        total_loss = 0.0

        try:
            for example in examples:
                program_output = program.interp(example.input_environment)
                loss = example.output_environment.distance(program_output)
                total_loss += loss
        except (InvalidTransition, MaxNumberOfIterationsExceededException, RecursiveCallLimitReached,
                LoopIterationLimitReached):
            raise InvalidProgramException

        return total_loss / len(examples)

    @staticmethod
    def compute_loss(resulting_envs: Tuple[Environment], wanted_envs: Tuple[Environment]):
        total_loss = 0.0
        try:
            for result_env, wanted_env in zip(resulting_envs, wanted_envs):
                loss = result_env.distance(wanted_env)
                total_loss += loss
        except (InvalidTransition, MaxNumberOfIterationsExceededException, RecursiveCallLimitReached,
                LoopIterationLimitReached):
            raise InvalidProgramException

        return total_loss / len(resulting_envs)

    @staticmethod
    def compute_max_expected_loss(examples: List[Example]):
        env = examples[0].input_environment
        if isinstance(env, RobotEnvironment):
            return examples[0].output_environment.distance(examples[0].input_environment)
        if isinstance(env, PixelEnvironment):
            return examples[0].output_environment.distance(examples[0].input_environment)
        if isinstance(env, StringEnvironment):
            return MCTS.compute_loss_of_program(Program([]), examples)

    def compute_urgency(self, node: SearchTreeNode) -> float:
        assert (node.number_of_visits > 0)

        # both are expected to be between 0 and 1
        average_reward = node.total_obtained_reward / node.number_of_visits
        # greatest_reward = node.greatest_obtained_reward

        # TODO see what happens when greatest_reward or a combo is used for exploitation_component
        exploitation_component = average_reward
        # exploitation_component = average_reward + (1 + self.get_average_token_score(node.chosen_token))
        exploration_component = 2.0 * EXPLORATION_CONSTANT * math.sqrt(
            2 * math.log(node.parent.number_of_visits) / node.number_of_visits)

        return exploitation_component + exploration_component

    def get_average_token_score(self, token: InventedToken):
        token_score = self.token_scores_dict[token]
        return token_score.score / token_score.visits

    @staticmethod
    def remove_nodes_with_no_possible_extensions(current_node: SearchTreeNode):
        """"When a node has no possibility to be (further) explored, this method can be used to remove all its
        ancestors that can also not be explored any more."""

        parent: SearchTreeNode = current_node.parent

        # remove the node from the tree
        current_node.parent = None

        parent_has_other_extensions: bool = len(parent.children) + len(parent.unexplored_succeeding_tokens) > 0

        # delete ancestors until you find a parent that still has a possibility for exploitation
        while not parent_has_other_extensions:
            current_node = parent
            parent = current_node.parent
            current_node.parent = None
            parent_has_other_extensions = len(parent.children) + len(parent.unexplored_succeeding_tokens) > 0

        # once a ancestor was found that has other possibilities for exploitation, update the number of visits
        parent.number_of_visits -= current_node.number_of_visits
        parent.total_obtained_reward -= current_node.total_obtained_reward
        if parent.greatest_obtained_reward == current_node.greatest_obtained_reward:
            obtained_rewards_by_children: List[float] = \
                list(map(lambda node: node.greatest_obtained_reward, parent.children))
            obtained_rewards_by_children.append(-1000.00)
            parent.greatest_obtained_reward = max(obtained_rewards_by_children)

        return

    def select(self, current_node: SearchTreeNode, current_program) -> Tuple[SearchTreeNode, Program]:

        # if current_node has unexplored actions, select current_node
        # if len(current_node.unexplored_succeeding_actions) > 0:
        if len(current_node.unexplored_succeeding_tokens) > 0:
            return current_node, current_program

        # else use tree policy to select child node with greatest urgency
        children: List[SearchTreeNode] = current_node.children

        assert (len(children) > 0)
        selected_child = None
        selected_child_urgency = -1000

        for child in children:
            urgency = self.compute_urgency(child)
            if urgency > selected_child_urgency:
                selected_child = child
                selected_child_urgency = urgency

        # Append the current_program with the token belonging to selected_child
        current_program.sequence.append(selected_child.chosen_token)

        return self.select(
            current_node=selected_child,
            current_program=current_program,
        )

    def expand(
            self,
            node: SearchTreeNode,
            program: Program,
    ) -> SearchTreeNode:
        """Expands the given node by selecting a token and creating a child node. This token is added to the given
        program. This new child node and appended program are returned."""

        # TODO use a better way to select the unexplored tokens
        selected_token = \
            node.unexplored_succeeding_tokens.popleft()

        # append the given program with the selected
        program.sequence.append(selected_token)

        new_node = SearchTreeNode(
            # program=new_program,
            chosen_token=selected_token,
            loss=1000,      # will be changed in simulation step
            unexplored_succeeding_tokens=deque(self.invented_tokens),
            number_of_visits=0,
            total_obtained_reward=0.0,
            greatest_obtained_reward=0.0,
            parent=node,
        )
        return new_node

    def simulate_and_return_reward(
            self,
            node: SearchTreeNode,
            program: Program,
    ) -> float:
        """Computes the loss and reward for the given program. Also updates the token_score of node.chosen_token based
        on this computed reward. Returns the reward."""
        try:
            # try interpreting the found program on the provided examples
            resulting_envs = MCTS.get_resulting_envs(
                program=program,
                input_envs=self.input_envs,
            )

            # TODO somehow check which one is shorter and keep that one. E.g. save node AND program length
            # check that the resulting_envs have not been found before and then add them to the dictionary
            if resulting_envs in self.dict_with_obtained_output_environments:

                # before raising exception, update token_score
                token_score = self.token_scores_dict[node.chosen_token]
                token_score.score += -1
                token_score.visits += 1

                raise SimilarProgramAlreadyFoundException("Another program resulting in the exact same output "
                                                          "environments was already found.")
            self.dict_with_obtained_output_environments[resulting_envs] = node

            loss = MCTS.compute_loss(resulting_envs, self.output_envs)
            node.loss = loss

            # update token_score
            parent: SearchTreeNode = node.parent
            token_score = self.token_scores_dict[node.chosen_token]
            if loss < parent.loss:
                token_score.score += 1
            elif loss > parent.loss:
                token_score.score -= 1
            token_score.visits += 1

            # check if the current program is beats self._best_program
            if loss < self.smallest_loss:
                # self._best_program = program
                self._best_program = program
                self.smallest_loss = loss

            # compute reward, which is expected to be between 0 and 1
            reward = 1.0 * (self.max_expected_loss - loss) / self.max_expected_loss
            assert (reward < 1.001)
            return reward

        # catch exceptions that are thrown upon interpreting the program
        except (InvalidTransition, MaxNumberOfIterationsExceededException, RecursiveCallLimitReached,
                LoopIterationLimitReached):

            # before raising exception, update token_score
            token_score = self.token_scores_dict[node.chosen_token]
            token_score.score += -1
            token_score.visits += 1

            raise InvalidProgramException

    def back_propagate(self, node: SearchTreeNode, reward: float):

        # else, update all relevant attributes
        node.number_of_visits += 1
        node.total_obtained_reward += reward
        if reward > node.greatest_obtained_reward:
            node.greatest_obtained_reward = reward

        # recursively do the same for all the ancestors of the current node.
        if node.parent is not None:
            self.back_propagate(node.parent, reward)

        return


if __name__ == "__main__":
    # node1 = SearchTreeNode(state="parent")
    # node2 = SearchTreeNode(state="child1", parent=node1)
    # node3 = SearchTreeNode(state="child2", parent=node1)
    # node4 = SearchTreeNode(state="grandparent", children=[node1])
    # node5 = SearchTreeNode(state="another child of granddad", parent=node4)
    # # node1.parent = None

    # node: SearchTreeNode
    # for pre, fill, node in RenderTree(node4):
    #     treestr = u"%s%s" % (pre, node.state)
    #     print(treestr.ljust(8), node, node.number_of_visits, node.total_obtained_reward)
    # print("\n")
    # print(str(node4))
    # print(str(node1.children))

    print("done!")
