import copy
from abc import abstractmethod
from enum import Enum
from typing import List, Union

from anytree import NodeMixin

from common_environment.abstract_tokens import TransToken, EnvToken, BoolToken, Token
from common_environment.environment import Environment
from search.MCTS.exceptions import IllegalActionException, ProgramAlreadyCompletedException, \
    TokenAlreadyCompletedException, ApplyingIncompleteTokenException, MaxNumberOfIterationsExceededException, \
    CannotInterpIncompleteProgram

# MAX_PROGRAM_DEPTH = 200
# MAX_SIMULATION_DEPTH = 3
LOOP_LIMIT = 100


# TODO do something with max program depth. This should happen throughout all the code.

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


class TokenType(Enum):
    BOOL_TOKEN = BoolToken
    ENV_TOKEN = EnvToken


class CompletableToken(EnvToken):
    """Token that, once completed, will return a environment.

    Attributes:
        completed -- Indicates whether the token is complete
        complete_action_allowed -- Indicates whether at this state it is okay to apply a CompleteAction

    It also has a function to retrieve what type of token is needed to expand the program"""

    @property
    @abstractmethod
    def completed(self):
        """Indicates whether the token is complete. AKA when no new tokens can be added anymore"""
        pass

    @property
    @abstractmethod
    def complete_action_allowed(self):
        """Indicates whether at this state it is okay to apply a CompleteAction. AKA when no new tokens are necessary"""
        pass

    def apply(self, env: Environment) -> Environment:
        """"Alters given environment and returns it. Raises an Exception if """
        raise NotImplementedError

    def get_needed_expand_token_type(self) -> TokenType:
        """Get TokenType that is Required for expanding this Token"""
        raise NotImplementedError

    def apply_action(self, action: Action):
        """Apply the given action. Raises an IllegalActionException if an illegal action was given"""
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class IfToken(CompletableToken):
    """If-token that needs other Tokens to complete its boolean condition and its body.
    Once completed it can be applied on a environment and it will return an environment.
    This If-token does NOT have an else body.

    Attributes:
        completed -- Indicates whether the token is complete
        complete_action_allowed -- Indicates whether at this state it is okay to apply an CompleteAction

    Methods:
        apply -- Applies the IfToken on an Environment and returns the altered Environment
        get_needed_expand_token_type -- Returns the TokenType that is needed for expanding the IfToken
        apply_action -- Apply either a CompleteAction or an ExpandAction to the IfToken.

    """

    def __init__(self):
        self._bool_condition: Union[BoolToken, None] = None
        self._body: Program = Program([], False, TokenType.ENV_TOKEN)

    @property
    def completed(self) -> bool:
        return self._body.complete

    @property
    def complete_action_allowed(self) -> bool:
        if not isinstance(self._bool_condition, BoolToken):
            return False

        return self._body.complete_action_allowed

    def apply(self, env: Environment) -> Environment:

        if not self.completed:
            raise ApplyingIncompleteTokenException("The IfToken you are trying to apply is not completed yet")

        boolean = self._bool_condition.apply(env)

        if boolean:
            return self._body.interp(env)

    def get_needed_expand_token_type(self) -> TokenType:
        if not isinstance(self._bool_condition, BoolToken):
            return TokenType.BOOL_TOKEN

        if not self._body.complete:
            return self._body.required_token_type_for_expansion

        raise TokenAlreadyCompletedException("The IfToken is already complete, "
                                             "so it is not possible to retrieve the needed_expand_token_type")

    def apply_action(self, action: Action):
        if self.completed:
            raise TokenAlreadyCompletedException("The IfToken is already complete, so no actions can be applied to it")

        # if the boolean condition is not set yet, only an Expand action with a BoolToken is allowed
        if not isinstance(self._bool_condition, BoolToken):
            if isinstance(action, ExpandAction):
                program_unit: ProgramUnit = action.program_unit
                if isinstance(program_unit.token, BoolToken):
                    self._bool_condition = program_unit.token
                    return

            raise IllegalActionException("ExpandAction with BoolToken is expected when applying an action on an "
                                         "IfToken with no boolean condition yet. Different action was received")

        # if the boolean condition has already been set, just try to apply the action on the body
        else:
            self._body.apply_action(action)

    def __repr__(self):
        return "IfToken(Condition: %s, Body: %s)" % (str(self._bool_condition), str(self._body))


class WhileToken(CompletableToken):
    """While-token that needs other Tokens to complete its boolean condition and its body.
    Once completed it can be applied on a environment and it will return an environment.

    Attributes:
        completed -- Indicates whether the token is complete
        complete_action_allowed -- Indicates whether at this state it is okay to apply an CompleteAction

    Methods:
        apply -- Applies the WhileToken on an Environment and returns the altered Environment
        get_needed_expand_token_type -- Returns the TokenType that is needed for expanding the WhileToken
        apply_action -- Apply either a CompleteAction or an ExpandAction to the WhileToken.

    """

    def __init__(self, max_number_of_iterations: int):
        self._bool_condition: Union[BoolToken, None] = None
        self._body: Program = Program([], False, TokenType.ENV_TOKEN)
        self._max_number_of_iterations: int = max_number_of_iterations

    @property
    def completed(self) -> bool:
        return self._body.complete

    @property
    def complete_action_allowed(self) -> bool:
        if not isinstance(self._bool_condition, BoolToken):
            return False

        return self._body.complete_action_allowed

    def apply(self, env: Environment) -> Environment:

        if not self.completed:
            raise ApplyingIncompleteTokenException("The WhileToken you are trying to apply is not completed yet")

        boolean = self._bool_condition.apply(env)
        iteration = 1

        while boolean and iteration <= self._max_number_of_iterations:
            # check if the max_number_of_iterations has not been exceeded
            if iteration > self._max_number_of_iterations:
                raise MaxNumberOfIterationsExceededException(
                    "The max_number_of_iterations was exceeded in the WhileLoop")

            # run the program in the body on the given environment
            env = self._body.interp(env)

            # update the boolean using the altered environment
            boolean = self._bool_condition.apply(env)

            # increment the number of iterations
            iteration += 1

        return env

    def get_needed_expand_token_type(self) -> TokenType:
        if not isinstance(self._bool_condition, BoolToken):
            return TokenType.BOOL_TOKEN

        if not self._body.complete:
            return self._body.required_token_type_for_expansion

        raise TokenAlreadyCompletedException("The WhileToken is already complete, "
                                             "so it is not possible to retrieve the needed_expand_token_type")

    def apply_action(self, action: Action):
        if self.completed:
            raise TokenAlreadyCompletedException("The IfToken is already complete, so no actions can be applied to it")

        # if the boolean condition is not set yet, only an Expand action with a BoolToken is allowed
        if not isinstance(self._bool_condition, BoolToken):
            if isinstance(action, ExpandAction):
                program_unit: ProgramUnit = action.program_unit
                if isinstance(program_unit.token, BoolToken):
                    self._bool_condition = program_unit.token
                    return

            raise IllegalActionException("ExpandAction with BoolToken is expected when applying an action on an "
                                         "WhileToken with no boolean condition yet. Different action was received")

        # if the boolean condition has already been set, just try to apply the action on the body
        else:
            self._body.apply_action(action)

    def __repr__(self):
        return "WhileToken(Condition: %s, Body: %s)" % (str(self._bool_condition), str(self._body))


class ProgramUnit(EnvToken):
    """Wrapper class for a token that also handles complete as well as incomplete tokens

     Methods: (selection of them)
         is_complete: indicates whether the token is complete
         apply_action: allows to apply an action to an incomplete ProgramUnit
     """

    def __init__(self, token: EnvToken):
        self.token = token

    def apply(self, env: Environment) -> Environment:
        return self.token.apply(env)

    def is_complete(self) -> bool:
        if isinstance(self.token, TransToken):
            return True
        elif isinstance(self.token, CompletableToken):
            return self.token.completed
        else:
            raise Exception("Something went wrong. Expected token to be either TransToken or CompletableToken")

    def complete_action_allowed(self) -> bool:
        if self.is_complete():
            raise TokenAlreadyCompletedException("Cannot complete a CompleteAction on a ProgramUnit that is already"
                                                 "complete, therefore question is redundant")
        if isinstance(self.token, CompletableToken):
            return self.token.complete_action_allowed

        raise Exception("Something went wrong. ProgramUnit should be either complete, or token should be "
                        "an instance of CompletableToken")

    def apply_action(self, action: Action):
        if self.is_complete():
            raise IllegalActionException("Action was applied to already completed ProgramUnit")
        elif isinstance(self.token, CompletableToken):
            self.token.apply_action(action)
            return
        else:
            raise Exception("Something went wrong. token should either be complete or instance of CompletableToken")


class Program(List[ProgramUnit]):
    """Wrapper class for a list of ProgramUnits, a program."""

    def __init__(
            self,
            program_units: List[ProgramUnit],
            complete: bool = False,
            required_token_type_for_expansion: TokenType = TokenType.ENV_TOKEN,
            loop_limit: int = LOOP_LIMIT
    ):
        """Creates a new program given a sequence of Tokens."""
        super().__init__()
        self.program = program_units
        self._complete = complete
        self.required_token_type_for_expansion = required_token_type_for_expansion
        self.loop_limit = loop_limit

    # def __gt__(self, other):
    #     if (self.number_of_tokens() > other.number_of_tokens()):
    #         return True
    #     else:
    #         return False

    @property
    def complete(self):
        return self._complete

    @property
    def complete_action_allowed(self) -> bool:
        # A Program which is already complete, will never allow a CompleteAction to be applied
        if self.complete:
            raise ProgramAlreadyCompletedException("The program is already complete, so redundant question was asked")

        # A Program should exist of at least one token before it can be completed
        if len(self.program) < 1:
            return False

        # If the last ProgramUnit is complete, the Program as a whole can be completed
        if self.program[-1].is_complete():
            return True

        # Else, the Program allows a CompleteAction if its last ProgramUnit allows this.
        return self.program[-1].complete_action_allowed()

    def interp(self, env: Environment, top_level_program=True, make_env_copy=True) -> Environment:
        """Interprets this program on a given Environment, returns the resulting Environment."""

        if not self.complete:
            raise CannotInterpIncompleteProgram("The program that you are trying to interp needs to be completed first")

        new_env = env

        if make_env_copy:
            new_env = copy.deepcopy(env)

        # Setup for recursive calls
        if top_level_program:
            new_env.program = self

        for program_unit in self.program:
            new_env = program_unit.apply(new_env)

        return new_env

    # def number_of_tokens(self) -> int:
    #     return sum([t.number_of_tokens() for t in self.sequence])

    def __repr__(self):
        return "Program([%s])" % ", ".join([str(token) for token in self.program])

    def to_formatted_string(self):
        return "Program:\n\t%s" % "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.program])

    def apply_action(self, action: Action):
        if self.complete:
            raise IllegalActionException("No actions can be applied on an already complete Program")

        if isinstance(action, CompleteAction) and self.program[-1].is_complete():
            # if the last ProgramUnit in the program is complete, the CompleteAction completes the program
            self._complete = True
            return

        # Else just try applying the Action on the last ProgramUnit
        else:
            self.program[-1].apply_action(action)
            return

    # def interp_cast(self, env: Environment):
    #   return cast(env, self.interp(env))


class SearchTreeNode(NodeMixin):
    def __init__(
            self,
            program: Program,
            unexplored_succeeding_actions: List[Action],
            preceding_action: Action = None,  # might not be necessary, but could be interesting for analyzing
            # max_program_depth_of_children: int = MAX_PROGRAM_DEPTH - 1,
            number_of_visits: int = 0,
            total_obtained_reward: int = 0,
            greatest_obtained_reward: int = 0,
            parent=None,
            children=None
    ):
        self.program = program
        self.unexplored_succeeding_actions = unexplored_succeeding_actions
        self.preceding_action = preceding_action
        # self.max_program_depth_of_children = max_program_depth_of_children
        self.number_of_visits = number_of_visits
        self.total_obtained_reward = total_obtained_reward
        self.greatest_obtained_reward = greatest_obtained_reward
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return "SearchTreeNode(Program: %s)" % self.program

    @staticmethod
    def initialize_search_tree(trans_tokens, loop_limit: int = LOOP_LIMIT):

        unexplored_actions: List[Action] = []

        for trans_token in trans_tokens:
            unexplored_actions.append(ExpandAction(trans_token()))

        unexplored_actions.append(ExpandAction(IfToken()))
        unexplored_actions.append(ExpandAction(WhileToken(max_number_of_iterations=loop_limit)))

        return SearchTreeNode(
            program=Program([]),
            unexplored_succeeding_actions=unexplored_actions,
        )
