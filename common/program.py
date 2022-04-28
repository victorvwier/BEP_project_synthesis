from common.environment.environment import Environment
from common.tokens.abstract_tokens import *
import copy


class Program:
    """Wrapper class for a list of Tokens, a program."""

    def __init__(self, tokens: list[EnvToken]):
        """Creates a new program given a sequence of Tokens."""
        self.sequence = tokens
    
    def __gt__(self, other):
        if self.number_of_tokens() > other.number_of_tokens():
            return True
        else:
            return False

    def interp(self, env: Environment) -> Environment:
        """Interprets this program on a given Environment, returns the resulting Environment."""
        nenv = copy.deepcopy(env)

        for t in self.sequence:
            if not isinstance(t, Token):
                print("NOOOO")

            nenv = t.apply(nenv)

        return nenv

    def number_of_tokens(self) -> int:
        return sum([t.number_of_tokens() for t in self.sequence])

    def __str__(self):
        return "Program([%s])" % ", ".join([str(t) for t in self.sequence])

    def to_formatted_string(self):
        return "Program:\n\t%s" % "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.sequence])

