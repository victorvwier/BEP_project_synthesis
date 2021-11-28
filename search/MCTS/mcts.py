import time
from typing import Tuple
from interpreter.interpreter import Token
from myparser.experiment import TestCase
from search.MCTS.datastructures import Program, SearchTreeNode
from search.abstract_search import SearchAlgorithm
from anytree import NodeMixin, RenderTree

MAX_SEARCH_TIME_IN_SEC = 60
# MAX_PROGRAM_DEPTH = 200
# MAX_SIMULATION_DEPTH = 3
LOOP_LIMIT = 100


class MCTS(SearchAlgorithm):

    def search(self, test_case: TestCase, trans_tokens: set[Token], bool_tokens: set[Token]) -> Tuple[
        Program, int, int]:

        # calculate the time that the algorithm should stop. 2 seconds are subtracted to make sure it stops in time
        max_finish_time = time.time() + MAX_SEARCH_TIME_IN_SEC - 2

        searchTree: SearchTreeNode = SearchTreeNode.initialize_search_tree(trans_tokens, )

        best_program_so_far : Program = Program([], complete=True)

        # TODO implement this
        while time.time() < max_finish_time

    # TODO do something with max program depth. This should happen throughout all the code.


if __name__ == "__main__":
    node1 = SearchTreeNode(state="parent")
    node2 = SearchTreeNode(state="child1", parent=node1)
    node3 = SearchTreeNode(state="child2", parent=node1)
    node4 = SearchTreeNode(state="grandparent", childeren=[node1])
    node5 = SearchTreeNode(state="another child of granddad", parent=node4)
    # node1.parent = None

    node: SearchTreeNode
    for pre, fill, node in RenderTree(node4):
        treestr = u"%s%s" % (pre, node.state)
        print(treestr.ljust(8), node, node.number_of_visits, node.total_obtained_reward)
    print("\n")
    print(str(node4))
    print(str(node1.children))
