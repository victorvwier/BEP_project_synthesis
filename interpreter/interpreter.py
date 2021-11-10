from common_environment.abstract_tokens import *
from common_environment.environment import *


class Program:
    def __init__(self, tokens: 'list[Token]'):
        self.sequence = tokens

    def interp(self, env: Environment):
        tokens = self.program.copy()
        while tokens[::1]:
            env = tokens.pop(0).apply(env)
        return env