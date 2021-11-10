from ..common_environment.abstract_tokens import *
from ..common_environment.environment import *

class If(ControlToken):
    def __init__(self, cond: BoolToken, e1: Token, e2: Token):
        self.cond = cond
        self.e1 = e1
        self.e2 = e2

    def apply(self, env: Environment):
        if self.cond.apply(env):
            return self.e1.apply(env)
        return self.e2.apply(env)