from common_environment.abstract_tokens import Token, Environment


class Program:
    """Wrapper class for a list of Tokens, a program."""

    def __init__(self, tokens: list[Token]):
        """Creates a new program given a sequence of Tokens."""
        self.sequence = tokens

    def interp(self, env: Environment):
        """Interprets this program on a given Environment, returns the resulting Environment."""
        tokens = self.sequence.copy()
        while tokens:
            env = tokens.pop(0).apply(env)
        return env

    #def interp_cast(self, env: Environment):
    #   return cast(env, self.interp(env))