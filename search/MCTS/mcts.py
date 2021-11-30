import copy
import math
from collections import deque
from typing import List, Union, Type

from common.environment import Environment, StringEnvironment, RobotEnvironment, PixelEnvironment
from common.experiment import Example
from common.tokens.abstract_tokens import Token, InvalidTransition

from search.MCTS.datastructures import MCTSProgram, SearchTreeNode, Action, CompleteAction, TokenType, IfToken, \
    ExpandAction, WhileToken
from search.MCTS.exceptions import MaxNumberOfIterationsExceededException
from search.abstract_search import SearchAlgorithm

# TODO do something with max program depth. This should happen throughout all the code.
# MAX_PROGRAM_DEPTH = 200
# MAX_SIMULATION_DEPTH = 3
LOOP_LIMIT = 100
EXPLORATION_CONSTANT = 1.0 / math.sqrt(2)


class MCTS(SearchAlgorithm):

    def __init__(self, time_limit_sec: float):
        super().__init__(time_limit_sec)
        self._best_program: MCTSProgram
        self.smallest_loss: float = float("inf")
        self.max_expected_loss: float = float("inf")    # is used for normalizing exploitation factor
        self.search_tree: Union[SearchTreeNode, None] = None

    # TODO make sure that the type of trans_ and bool_token is set[Type[Token]] and not set[Token]
    def setup(self, training_examples: List[Example], trans_tokens: set[Type[Token]], bool_tokens: set[Type[Token]]):

        # set the best program to be an empty token list and calculate the associated loss
        self._best_program = MCTSProgram([], complete=True)
        self.smallest_loss = MCTS.compute_loss_of_program(self._best_program, training_examples)

        # set the max_expected_loss, which will be used to normalize the exploitation factor in the UCT
        self.max_expected_loss = MCTS.compute_max_expected_loss(training_examples)

        # initialize the root of the search tree
        self.search_tree: SearchTreeNode = \
            SearchTreeNode.initialize_search_tree(trans_tokens=trans_tokens, loop_limit=LOOP_LIMIT)

    # TODO make sure that the type of trans_ and bool_token is set[Type[Token]] and not set[Token]
    def iteration(self, training_example: List[Example], trans_tokens: set[Type[Token]], bool_tokens: set[Type[Token]]) \
            -> bool:

        # return False to indicate no other iterations are necessary
        if self.smallest_loss <= 0.001:
            return False

        # TODO implement the following subprocesses
        selected_node = MCTS.select(self.search_tree)
        MCTS.expand(selected_node, trans_tokens, bool_tokens)
        self.simulate()
        self.back_propagate()

        # return True to indicate that another iteration is required
        return True

    @staticmethod
    def compute_loss_of_program(program: MCTSProgram, examples: List[Example]) -> float:
        """Gets the average loss function of applying the program to each example.
        Returns float number equal to infinity if one of the examples could not be interpreted with the program"""

        total_loss = 0.0

        try:
            for example in examples:
                program_output = program.interp(example.input_environment)
                loss = example.output_environment.distance(program_output)
                total_loss += loss
        except (InvalidTransition, MaxNumberOfIterationsExceededException) as e:
            return float("inf")

        return total_loss / len(examples)

    @staticmethod
    def compute_max_expected_loss(examples: List[Example]):
        env = examples[0].input_environment
        if isinstance(env, RobotEnvironment):
            return examples[0].output_environment.distance(examples[0].input_environment)
        if isinstance(env, PixelEnvironment):
            return examples[0].output_environment.distance(examples[0].input_environment)
        if isinstance(env, StringEnvironment):
            return MCTS.compute_loss_of_program(MCTSProgram([], complete=True), examples)

    @staticmethod
    def compute_urgency(node: SearchTreeNode) -> float:
        assert(node.number_of_visits > 0)

        # both are expected to be between 0 and 1
        average_reward = node.total_obtained_reward / node.number_of_visits
        greatest_reward = node.greatest_obtained_reward

        # TODO see what happens when greatest_reward or a combo is used for exploitation_component
        exploitation_component = average_reward
        exploration_component = 2.0 * EXPLORATION_CONSTANT * math.sqrt(
            2 * math.log(node.parent.number_of_visits) / node.number_of_visits)

        return exploitation_component + exploration_component

    @staticmethod
    def select(current_node: SearchTreeNode) -> SearchTreeNode:

        # if current_node has unexplored actions, select current_node
        if len(current_node.unexplored_succeeding_actions) > 0:
            return current_node

        # else use tree policy to select child node with greatest urgency
        children = current_node.children
        # TODO make sure the situation that a node has no children does not appear or is taken care of
        assert (len(children) > 0)
        selected_child = None
        selected_child_urgency = -1000

        for child in children:
            urgency = MCTS.compute_urgency(child)
            if urgency > selected_child_urgency:
                selected_child = child
                selected_child_urgency = urgency

        return MCTS.select(selected_child)

    @staticmethod
    def expand(node: SearchTreeNode, trans_tokens: set[Type[Token]], bool_tokens: set[Type[Token]]) -> SearchTreeNode:
        """Expands the given node by creating a child node from an unexplored action. This child node is returned"""

        # TODO if making deepcopy is to time intensive, it is also possible to make program while selecting nodes
        selected_action = \
            node.unexplored_succeeding_actions.popleft()
        new_program: MCTSProgram = copy.deepcopy(node.program).apply_action(selected_action)

        # make list of all possible actions
        new_possible_actions: deque[Action] = deque([])
        required_token_type = new_program.required_token_type_for_expansion
        if new_program.complete_action_allowed:
            new_possible_actions.append(CompleteAction())
        if required_token_type == TokenType.BOOL_TOKEN:
            for token in bool_tokens:
                new_possible_actions.append(ExpandAction(token()))
        else:
            for token in trans_tokens:
                new_possible_actions.append(ExpandAction(token()))
            new_possible_actions.append(ExpandAction(IfToken()))
            new_possible_actions.append(ExpandAction(WhileToken(max_number_of_iterations=LOOP_LIMIT)))

        new_node = SearchTreeNode(
            program=new_program,
            unexplored_succeeding_actions=new_possible_actions,
            preceding_action=selected_action,
            number_of_visits=0,
            total_obtained_reward=0,
            greatest_obtained_reward=0,
            parent=node,
        )
        return new_node

    def simulate(self):
        # TODO implement()
        pass

    def back_propagate(self):
        # TODO implement
        pass


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