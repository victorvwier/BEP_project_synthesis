# import copy
import math
# import random
from collections import deque
from typing import List, Union, Type, Tuple, Dict

from common.environment import StringEnvironment, RobotEnvironment, PixelEnvironment, Environment
from common.experiment import Example
from common.prorgam import Program
from common.tokens.abstract_tokens import TransToken, BoolToken, InvalidTransition, InventedToken
from common.tokens.control_tokens import RecursiveCallLimitReached, LoopIterationLimitReached

from search.MCTS.datastructures import MCTSProgram, SearchTreeNode
from search.MCTS.exceptions import MaxNumberOfIterationsExceededException, InvalidProgramException, \
    SimilarProgramAlreadyFoundException
from search.abstract_search import SearchAlgorithm

# TODO do something with max program depth. This should happen throughout all the code.
# MAX_PROGRAM_DEPTH = 200
# MAX_SIMULATION_DEPTH = 3
from search.invent import invent2

LOOP_LIMIT = 100
EXPLORATION_CONSTANT = 1.0 / math.sqrt(2)
MAX_TOKEN_DEPTH = 3


def deepcopy_program(program: Program) -> Program:
    return Program(
        tokens=[token for token in program.sequence],
        recurse_limit=program.recursive_call_limit,
        loop_limit=program.loop_limit,
    )


class MCTS(SearchAlgorithm):

    def __init__(self, time_limit_sec: float):
        super().__init__(time_limit_sec)
        self._best_program: MCTSProgram
        self.smallest_loss: float = float("inf")
        self.max_expected_loss: float = float("inf")  # is used for normalizing exploitation factor
        self.search_tree: Union[SearchTreeNode, None] = None
        self.invented_tokens = List[InventedToken]
        self.input_envs: Tuple[Environment]
        self.output_envs: Tuple[Environment]
        self.dict_with_obtained_output_environments: Dict[Tuple[Environment], SearchTreeNode] = {}

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
        # self.max_expected_loss = MCTS.compute_max_expected_loss(training_examples)
        self.max_expected_loss = self.smallest_loss

        # compute invented tokens that are composed of several other tokens
        self.invented_tokens: List[InventedToken] = \
            invent2(tokenSet=trans_tokens, boolTokenSet=bool_tokens, maxLength=MAX_TOKEN_DEPTH)

        # initialize the root of the search tree
        self.search_tree: SearchTreeNode = \
            SearchTreeNode.initialize_search_tree(env_tokens=deque(self.invented_tokens))

        # initialize a dictionary that keeps track of outcomes of programs
        self.dict_with_obtained_output_environments[resulting_envs] = self.search_tree

    # TODO make sure that the type of trans_ and bool_token is set[Type[Token]] and not set[Token]
    def iteration(self, training_example: List[Example], trans_tokens: set[Type[TransToken]],
                  bool_tokens: set[Type[BoolToken]]) -> bool:

        # return False to indicate no other iterations are necessary
        if self.smallest_loss <= 0.001:
            return False

        # TODO implement the following subprocesses
        selected_node = MCTS.select(self.search_tree)
        new_node = self.expand(
            node=selected_node,
            # trans_tokens,
            # bool_tokens
        )
        try:
            reward = self.simulate_and_return_reward(
                node=new_node,
                # examples=training_example,
                # trans_tokens=trans_tokens,
                # bool_tokens=bool_tokens,
            )
            self.back_propagate(new_node, reward)
        except (InvalidProgramException, SimilarProgramAlreadyFoundException):
            # TODO possibly have different strategy for when a similar program was already found
            MCTS.remove_nodes_with_no_possible_extensions(new_node)

        # return True to indicate that another iteration is required
        return True

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

    @staticmethod
    def compute_urgency(node: SearchTreeNode) -> float:
        assert (node.number_of_visits > 0)

        # both are expected to be between 0 and 1
        average_reward = node.total_obtained_reward / node.number_of_visits
        # greatest_reward = node.greatest_obtained_reward

        # TODO see what happens when greatest_reward or a combo is used for exploitation_component
        exploitation_component = average_reward
        exploration_component = 2.0 * EXPLORATION_CONSTANT * math.sqrt(
            2 * math.log(node.parent.number_of_visits) / node.number_of_visits)

        return exploitation_component + exploration_component

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

    @staticmethod
    def select(current_node: SearchTreeNode) -> SearchTreeNode:

        # if current_node has unexplored actions, select current_node
        # if len(current_node.unexplored_succeeding_actions) > 0:
        if len(current_node.unexplored_succeeding_tokens) > 0:
            return current_node

        # else use tree policy to select child node with greatest urgency
        children = current_node.children

        assert (len(children) > 0)
        selected_child = None
        selected_child_urgency = -1000

        for child in children:
            urgency = MCTS.compute_urgency(child)
            if urgency > selected_child_urgency:
                selected_child = child
                selected_child_urgency = urgency

        return MCTS.select(selected_child)

    # @staticmethod
    def expand(
            self,
            node: SearchTreeNode,
            # trans_tokens: set[Type[TransToken]],
            # bool_tokens: set[Type[BoolToken]]
    ) -> SearchTreeNode:
        """Expands the given node by creating a child node from an unexplored action. This child node is returned"""

        # TODO if making deepcopy is to time intensive, it is also possible to make program while selecting nodes
        selected_token = \
            node.unexplored_succeeding_tokens.pop()
        new_program: Program = deepcopy_program(node.program)
        new_program.sequence.append(selected_token)

        # # if the applied action completed the program, there are no possible succeeding actions
        # if new_program.complete:
        #     return SearchTreeNode(
        #         program=new_program,
        #         unexplored_succeeding_tokens=deque([]),
        #         # preceding_action=selected_action,
        #         number_of_visits=0,
        #         total_obtained_reward=0.0,
        #         greatest_obtained_reward=0.0,
        #         parent=node,
        #     )

        # else, make list of all possible actions
        # new_possible_actions: deque[Action] = deque([])
        # required_token_type = new_program.required_token_type_for_expansion
        # if new_program.complete_action_allowed:
        #     new_possible_actions.append(CompleteAction())
        # if required_token_type == TokenType.BOOL_TOKEN:
        #     for token in bool_tokens:
        #         new_possible_actions.append(ExpandAction(token()))
        # else:
        #     for token in trans_tokens:
        #         new_possible_actions.append(ExpandAction(ProgramUnit(token())))
        #     new_possible_actions.append(ExpandAction(ProgramUnit(IfToken())))
        #     new_possible_actions.append(ExpandAction(ProgramUnit(WhileToken(max_number_of_iterations=LOOP_LIMIT))))
        # new_possible_succeeding_tokens = deque([])
        # for token in self.invented_tokens:
        #     new_possible_succeeding_tokens.append(token)

        new_node = SearchTreeNode(
            program=new_program,
            # unexplored_succeeding_actions=new_possible_actions,
            # preceding_action=selected_action,
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
            # examples: List[Example],
            # trans_tokens: set[Type[TransToken]],
            # bool_tokens: set[Type[BoolToken]]
    ) -> float:

        try:
            # try interpreting the found program on the provided examples
            resulting_envs = MCTS.get_resulting_envs(
                program=node.program,
                input_envs=self.input_envs,
            )

            # check that the resulting_envs have not been found before and then add them to the dictionary
            if resulting_envs in self.dict_with_obtained_output_environments:
                raise SimilarProgramAlreadyFoundException("Another program resulting in the exact same output "
                                                          "environments was already found.")
            self.dict_with_obtained_output_environments[resulting_envs] = node

            loss = MCTS.compute_loss(resulting_envs, self.output_envs)

            # check if the current program is beats self._best_program
            if loss < self.smallest_loss:
                # self._best_program = program
                self._best_program = node.program
                self.smallest_loss = loss

            # compute reward, which is expected to be between 0 and 1
            reward = 1.0 * (self.max_expected_loss - loss) / self.max_expected_loss
            assert (reward < 1.001)
            return reward

        # catch exceptions that are thrown upon interpreting the program
        except (InvalidTransition, MaxNumberOfIterationsExceededException, RecursiveCallLimitReached,
                LoopIterationLimitReached):
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
