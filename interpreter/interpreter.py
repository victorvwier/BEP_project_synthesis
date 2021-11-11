from common_environment.abstract_tokens import Token, Environment

class Program:
    """Wrapper class for a list of Tokens, a program."""

    def __init__(self, tokens: 'list[Token]'):
        """Creates a new program given a sequence of Tokens."""
        self.sequence = tokens

    def interp(self, env: Environment, top_level_program = True) -> Environment:
        """Interprets this program on a given Environment, returns the resulting Environment."""

        # Setup for recursive calls
        if top_level_program:
            env.program = self

        tokens = self.sequence.copy()
        while tokens:
            env = tokens.pop(0).apply(env)
        return env

    #def interp_cast(self, env: Environment):
    #   return cast(env, self.interp(env))