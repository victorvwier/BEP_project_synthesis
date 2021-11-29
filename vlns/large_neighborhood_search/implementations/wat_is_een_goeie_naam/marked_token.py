from common_environment.abstract_tokens import Token, Environment, EnvToken, BoolToken


class MarkedToken(Token):
    """Abstract MarkedToken token is marked for destruction. However the previous token is contained to evaluate the
    program as it used to be."""

    def __init__(self, old_token: Token):
        self.old_token = old_token

    def apply(self, env: Environment):
        return self.old_token.apply(env)

    def __str__(self):
        return "Marked({})".format(self.old_token.__str__())


class MarkedEnvToken(MarkedToken, EnvToken):
    """Token that marks that an EnvToken is up for destruction."""
    pass


class MarkedBoolToken(MarkedToken, BoolToken):
    """Token that marks that an EnvToken is up for destruction."""
    pass


class IdToken(EnvToken):

    def apply(self, env: Environment):
        return env
