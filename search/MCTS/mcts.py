import copy
import time
from typing import Tuple, List, Union

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


class MCTS(SearchAlgorithm):

    def __init__(self, time_limit_sec: float):
        super().__init__(time_limit_sec)
        self._best_program: MCTSProgram
        self.smallest_loss: float = float("inf")
        self.search_tree: Union[SearchTreeNode, None] = None     # this one gets initialised when calling run

    def setup(self, training_examples: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]):

        # set the best program to be an empty token list and calculate the associated loss
        self._best_program = MCTSProgram([], complete=True)
        self.smallest_loss = MCTS.get_loss_of_program(self._best_program, training_examples)

        # initialize the root of the search tree
        self.search_tree: SearchTreeNode = \
            SearchTreeNode.initialize_search_tree(trans_tokens=trans_tokens, loop_limit=LOOP_LIMIT)

    def iteration(self, training_example: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]) -> bool:

        # return False to indicate no other iterations are necessary
        if self.smallest_loss <= 0.001:
            return False

        # TODO implement the following subprocesses
        selected_node = self.select(self.search_tree)
        self.expand()
        self.simulate()
        self.back_propagate()

        # return True to indicate that another iteration is required
        return True

    @staticmethod
    def get_loss_of_program(program: MCTSProgram, examples: List[Example]) -> float:
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
        #
        # # select an unexplored action if possible
        # if len(current_node.unexplored_succeeding_actions) > 0:
        #     # TODO if making deepcopy is to time intensive, it is also possible to make program while selecting nodes
        #     selected_action = \
        #         current_node.unexplored_succeeding_actions.pop(0)   # TODO use queue for popping for better performance
        #     new_program: MCTSProgram = copy.deepcopy(current_node.program).apply_action(selected_action)
        #
        #     # make list of all possible actions
        #     new_possible_actions: List[Action] = []
        #     required_token_type = new_program.required_token_type_for_expansion
        #     if new_program.complete_action_allowed:
        #         new_possible_actions.append(CompleteAction())
        #     if required_token_type == TokenType.BOOL_TOKEN:
        #         for token in self.bool_tokens:
        #             new_possible_actions.append(ExpandAction(token()))
        #     else:
        #         for token in self.trans_tokens:
        #             new_possible_actions.append(ExpandAction(token()))
        #         new_possible_actions.append(ExpandAction(IfToken()))
        #         new_possible_actions.append(ExpandAction(WhileToken(max_number_of_iterations=self.loop_limit)))
        #
        #     new_node = SearchTreeNode(
        #         program=new_program,
        #         unexplored_succeeding_actions=new_possible_actions,
        #         preceding_action=selected_action,
        #         number_of_visits=0,
        #         total_obtained_reward=0,
        #         greatest_obtained_reward=0,
        #         parent=current_node,
        #     )
        #     return new_node
        #
        # # else use tree policy to select child node with greatest urgency
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
