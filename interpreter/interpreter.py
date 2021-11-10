from common_environment.abstract_tokens import Token, Environment


class Program:
    def __init__(self, tokens: list[Token]):
        self.sequence = tokens

    def interp(self, env: Environment):
        tokens = self.sequence.copy()
        while tokens[::1]:
            env = tokens.pop(0).apply(env)
        return env