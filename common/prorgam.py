from common.tokens.abstract_tokens import *
import copy


class Program:
    """Wrapper class for a list of Tokens, a program."""

    def __init__(self, tokens: list[EnvToken], recurse_limit: int = 300, loop_limit: int = 100):
        """Creates a new program given a sequence of Tokens."""
        self.sequence = tokens
        self.recursive_call_limit = recurse_limit
        self.loop_limit = loop_limit
    
    def __gt__(self, other):
        if self.number_of_tokens() > other.number_of_tokens():
            return True
        else:
            return False

    def interp(self, env: Environment, top_level_program=True) -> Environment:
        """Interprets this program on a given Environment, returns the resulting Environment."""
        nenv = copy.deepcopy(env)

        # Setup for recursive calls
        if top_level_program:
            nenv.program = self

        for t in self.sequence:
            if(not isinstance(t, Token)):
                print("NOOOO")
            nenv = t.apply(nenv)

        return nenv

    def number_of_tokens(self) -> int:
        return sum([t.number_of_tokens() for t in self.sequence])

    def __str__(self):
        return "Program([%s])" % ", ".join([str(t) for t in self.sequence])

    def to_formatted_string(self):
        return "Program:\n\t%s" % "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.sequence])

    # def interp_cast(self, env: Environment):
    #   return cast(env, self.interp(env))
