from typing import Union

from common_environment.abstract_tokens import *
from common_environment.environment import *
from interpreter import *

class If(ControlToken):
    """If statement ControlToken."""

    def __init__(self, cond: BoolToken, e1: Token, e2: Token):
        """Creates a new If ControlToken. When applied, 'cond' is executed. If that yields true, 'e1' is execute, otherwise 'e2'."""
        self.cond = cond
        self.e1 = e1
        self.e2 = e2

    def apply(self, env: Environment) -> Environment:
        if self.cond.apply(env):
            return self.e1.apply(env)
        return self.e2.apply(env)

class Recurse(ControlToken):
    """Recursive calling ControlToken."""

    def __init__(self, cond: BoolToken, base_case: List[Token], recursive_case: List[Token], program: Program):
        """Creates a new Recurse ControlToken. When applied, 'cond' is executed. If that yields true, 'recursive_case' is executed and the whole program is called recursively, otherwise 'base_case' is executed. Note that this Token needs a pointer to its parent program to be able to call it recursively."""
        self.cond = cond
        self.base_case = base_case
        self.recursive_case = recursive_case
        self.program = program

    def apply(self, env: Environment) -> Environment:
        if self.cond.apply(env):
            self.env = Program(self.recursive_case).interp(env)
            return self.program.interp(env)
        return Program(self.base_case).interp(env)