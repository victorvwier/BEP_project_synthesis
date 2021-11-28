import copy
import time
from typing import Tuple, List, Union

from common_environment.abstract_tokens import InvalidTransition
from interpreter.interpreter import Token
from myparser.experiment import TestCase, Example
from search.MCTS.datastructures import Program, SearchTreeNode, Action, CompleteAction, TokenType, IfToken, \
    ExpandAction, WhileToken
from search.MCTS.exceptions import MaxNumberOfIterationsExceededException
from search.abstract_search import SearchAlgorithm
# from anytree import NodeMixin, RenderTree

# TODO do something with max program depth. This should happen throughout all the code.
MAX_SEARCH_TIME_IN_SEC = 60
# MAX_PROGRAM_DEPTH = 200
# MAX_SIMULATION_DEPTH = 3
LOOP_LIMIT = 100


class MCTS(SearchAlgorithm):

    def search(
            test_case: TestCase,
            trans_tokens: set[Token],
            bool_tokens: set[Token]
    ) -> Tuple[Program, int, int]:
        return MCTSProcess(
            training_examples=test_case.training_examples,
            trans_tokens=trans_tokens,
            bool_tokens=bool_tokens,
            loop_limit=LOOP_LIMIT,
            max_search_time_in_seconds=MAX_SEARCH_TIME_IN_SEC,
        ).run()


class MCTSProcess:
    """Initializes a search process and returns the best found Program within the given maximum search time"""

    def __init__(
            self,
            training_examples: List[Example],
            trans_tokens: set[Token],
            bool_tokens: set[Token],
            max_search_time_in_seconds: int,
            loop_limit: int = LOOP_LIMIT
    ):
        self.training_examples = training_examples
        self.trans_tokens = trans_tokens
        self.bool_tokens = bool_tokens
        self.max_search_time_in_seconds = max_search_time_in_seconds
        self.loop_limit = loop_limit
        self.best_program_so_far = Program([], complete=True)
        self.smallest_loss_so_far = MCTSProcess.get_loss_of_program(self.best_program_so_far, training_examples)
        self.search_tree: Union[SearchTreeNode, None] = None     # this one gets initialised when calling run


    def run(self) -> Tuple[Program, int, int]:
        # calculate the time that the algorithm should stop. 2 seconds are subtracted to make sure it stops in time
        max_finish_time = time.time() + self.max_search_time_in_seconds - 2

        # initialize the root of the search tree
        self.search_tree: SearchTreeNode = \
            SearchTreeNode.initialize_search_tree(self.trans_tokens, loop_limit=self.loop_limit)

        while time.time() < max_finish_time and self.smallest_loss_so_far > 0.001:
            # TODO implement the following subprocesses
            selected_node = self.select(self.search_tree)
            self.expand()
            self.simulate()
            self.back_propagate()

        return self.best_program_so_far, int(self.smallest_loss_so_far), int(self.smallest_loss_so_far <= 0.001)

    @staticmethod
    def get_loss_of_program(program: Program, examples: List[Example]) -> float:
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

    def select(self, current_node: SearchTreeNode) -> SearchTreeNode:

        # select an unexplored action if possible
        if len(current_node.unexplored_succeeding_actions) > 0:
            # TODO if making deepcopy is to time intensive, it is also possible to make program while selecting nodes
            selected_action = \
                current_node.unexplored_succeeding_actions.pop(0)   # TODO use queue for popping for better performance
            new_program: Program = copy.deepcopy(current_node.program).apply_action(selected_action)

            # make list of all possible actions
            new_possible_actions: List[Action] = []
            required_token_type = new_program.required_token_type_for_expansion
            if new_program.complete_action_allowed:
                new_possible_actions.append(CompleteAction())
            if required_token_type == TokenType.BOOL_TOKEN:
                for token in self.bool_tokens:
                    new_possible_actions.append(ExpandAction(token()))
            else:
                for token in self.trans_tokens:
                    new_possible_actions.append(ExpandAction(token()))
                new_possible_actions.append(ExpandAction(IfToken()))
                new_possible_actions.append(ExpandAction(WhileToken(max_number_of_iterations=self.loop_limit)))

            new_node = SearchTreeNode(
                program=new_program,
                unexplored_succeeding_actions=new_possible_actions,
                preceding_action=selected_action,
                number_of_visits=0,
                total_obtained_reward=0,
                greatest_obtained_reward=0,
                parent=current_node,
            )
            return new_node

        # else use tree policy to select child node with greatest urgency
        # TODO implement
        pass

    def expand(self):
        # TODO implement
        pass

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
    # node4 = SearchTreeNode(state="grandparent", childeren=[node1])
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
