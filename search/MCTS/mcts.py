import copy
from enum import Enum
from typing import Tuple, List, Union
from interpreter.interpreter import Token, EnvToken, Environment, TransToken, BoolToken
from myparser.experiment import TestCase
from search.abstract_search import SearchAlgorithm
from anytree import NodeMixin, RenderTree

MAX_SEARCH_TIME_IN_SEC = 60
MAX_PROGRAM_DEPTH = 200
MAX_SIMULATION_DEPTH = 3
RECURSION_LIMIT = 100
LOOP_LIMIT = RECURSION_LIMIT

class Action(object):
    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return "Action(description: %s)" % self.description

class CompleteAction(Action):
    def __init__(self):
        super().__init__(description="Declare Program Complete")

class ExpandAction(Action):
    def __init__(self, program_unit: Token):
        super().__init__(description="Expand Program with: %s" % str(program_unit))
        self.program_unit = program_unit

class IllegalActionException(Exception):
    """Raised when an illegal Action is applied to a Completable Token or a Program"""
    pass

class TokenType(Enum):
    BOOL_TOKEN = BoolToken
    ENV_TOKEN = EnvToken

class CompletableToken(EnvToken):
    """Token that, once completed, will return a environment.

    Attributes:
        completed -- Indicates whether the action is complete
        complete_action_allowed -- Indicates whether at this state it is okay to apply an CompleteAction

    It also has a function to retrieve what type of token is needed to expand the program"""

    def apply(self, env: Environment) -> Environment:
        """"Alters given environment and returns it. Raises an Exception if """
        raise NotImplementedError

    def __init__(self):
        self.completed = False
        self.complete_action_allowed = False
    # def make_complete(self):
    #     """Sets complete to True if it could be applied to an environment.
    #     Raises an exception if it still needs an expansion before it can be applied"""
    #     raise NotImplementedError

    def get_needed_expand_token_type(self) -> TokenType:
        """Get TokenType that is Required for expanding this Token"""
        raise NotImplementedError

    def apply_action(self, action: Action):
        """Apply the given action. Raises an IllegalActionException if an illegal action was given"""
        raise NotImplementedError

class ProgramUnit(EnvToken):
    """Wrapper class for a token, which  indicates whether the token is complete and provides """

    def __init__(self, token: EnvToken):
        self.token = token

        if isinstance(token, TransToken):
            self.completed = True
        if isinstance(self.token, CompletableToken):
            self.completed = False

    def apply(self, env: Environment) -> Environment:
        return self.token.apply(env)

    # def make_complete(self):
    #     """Tries declaring the program unit as complete"""
    #     if self.completed:
    #         return
    #     if isinstance(self.token, CompletableToken)
    #     self.token.make_complete()

    def apply_action(self, action: Action):
        if self.completed:
            raise IllegalActionException("Action was applied to already completed ProgramUnit")
        elif isinstance(self.token, CompletableToken):
            self.token.apply_action(action)
        else:
            raise Exception("Something went wrong. token should either be complete or instance of CompletableToken")


class Program:
    """Wrapper class for a list of ProgramUnits, a program."""

    def __init__(self, program_units: List[ProgramUnit], complete: bool, required_token_type_for_expansion: TokenType, recurse_limit: int = RECURSION_LIMIT, loop_limit: int = LOOP_LIMIT):
        """Creates a new program given a sequence of Tokens."""
        self.program = program_units
        self.complete = complete
        self.required_token_type_for_expansion = required_token_type_for_expansion
        self.recursive_call_limit = recurse_limit
        self.loop_limit = loop_limit

    # def __gt__(self, other):
    #     if (self.number_of_tokens() > other.number_of_tokens()):
    #         return True
    #     else:
    #         return False

    def interp(self, env: Environment, top_level_program=True) -> Environment:
        """Interprets this program on a given Environment, returns the resulting Environment."""

        new_env = copy.deepcopy(env)

        # Setup for recursive calls
        if top_level_program:
            new_env.program = self

        # TODO do something in case the program is not complete

        for program_unit in self.program:
            new_env = program_unit.apply(new_env)

        return new_env

    # def number_of_tokens(self) -> int:
    #     return sum([t.number_of_tokens() for t in self.sequence])

    def __str__(self):
        return "Program([%s])" % ", ".join([str(t) for t in self.sequence])

    def to_formatted_string(self):
        return "Program:\n\t%s" % "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.sequence])

    # def interp_cast(self, env: Environment):
    #   return cast(env, self.interp(env))




class SearchTreeNode(NodeMixin):
    def __init__(
            self,
            program: Program,
            unexplored_succeeding_actions: List[Action],
            preceding_action: Action = None,  # might not be necessary, but could be interesting for analyzing
            max_program_depth_of_children: int = MAX_PROGRAM_DEPTH-1,
            number_of_visits: int = 0,
            total_obtained_reward: int = 0,
            greatest_obtained_reward: int = 0,
            parent=None,
            children=None
    ):
        self.program = program
        self.unexplored_succeeding_actions = unexplored_succeeding_actions
        self.preceding_action = preceding_action
        self.max_program_depth_of_children = max_program_depth_of_children
        self.number_of_visits = number_of_visits
        self.total_obtained_reward = total_obtained_reward
        self.greatest_obtained_reward = greatest_obtained_reward
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return "SearchTreeNode(Program: %s)" % self.program

    @staticmethod
    def initialize_search_tree(trans_tokens):
        return SearchTreeNode(
            program = [],
            unexplored_succeeding_actions: trans_token.action,
        preceding_action: Action = None,  # might not be necessary, but could be interesting for analyzing
                                   max_program_depth_of_children: int = MAX_PROGRAM_DEPTH - 1,
                                                                        number_of_visits: int = 0,
                                                                                                total_obtained_reward: int = 0,
                                                                                                                             greatest_obtained_reward: int = 0,
                                                                                                                                                             parent = None,
                                                                                                                                                                      children = None
        )


class MCTS(SearchAlgorithm):

    def search(self, test_case: TestCase, trans_tokens: set[Token], bool_tokens: set[Token]) -> Tuple[Program, int, int]:
        searchTree: SearchTreeNode = initialize_search_tree(trans_tokens, bool_tokens)


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
