from typing import List, Union

from common_environment.abstract_tokens import ControlToken, BoolToken, Token, Environment
from interpreter.interpreter import Program


class If(ControlToken):
    """If statement ControlToken."""

    def __init__(self, cond: BoolToken, e1: List[Token], e2: List[Token]):
        """Creates a new If ControlToken. When applied, 'cond' is executed. If that yields true, 'e1' is execute, otherwise 'e2'."""
        self.cond = cond
        self.e1 = e1
        self.e2 = e2

    def apply(self, env: Environment) -> Environment:
        if self.cond.apply(env):
            return Program(self.e1).interp(env, False)
        return Program(self.e2).interp(env, False)

class Recurse(ControlToken):
    """Recursive calling ControlToken."""

    def __init__(self, cond: Union[None, BoolToken], base_case: List[Token], recursive_case: List[Token]):
        """Creates a new Recurse ControlToken. When applied, 'cond' is executed. If that yields true, 'recursive_case' is executed and the whole program is called recursively, otherwise 'base_case' is executed. Note that this Token needs a pointer to its parent program to be able to call it recursively."""
        self.cond = cond
        self.base_case = base_case
        self.recursive_case = recursive_case
        self.calls = 0

    def apply(self, env: Environment) -> Environment:
        # Raise exception if recursive call limit is reached
        if self.calls >= env.program.recursive_call_limit:
            raise RecursiveCallLimitReached()

        self.calls += 1

        # if the condition is None or true, make recursive call
        if self.cond is None or self.cond.apply(env):
            env = Program(self.recursive_case).interp(env, False)
            return env.program.interp(env)

        # else, base case
        return Program(self.base_case).interp(env, False)

class RecursiveCallLimitReached(Exception):
    """"Exception raised when the recursive call limit, set in the Program constructor is reached."""
    pass