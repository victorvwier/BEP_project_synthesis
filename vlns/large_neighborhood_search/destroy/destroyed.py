from common_environment.abstract_tokens import Token, EnvToken
from common_environment.environment import Environment


class DestroyedToken(Token):
    """Contains a token marked as destroyed."""

    def __init__(self, destroyed_token: Token):
        self.destroyed_token = destroyed_token

    def apply(self, env: Environment):
        return self.destroyed_token.apply(env)

    def __str__(self):
        return "Destroyed({})".format(self.destroyed_token)


class DiscardToken(EnvToken):

    def apply(self, env: Environment):
        return env
