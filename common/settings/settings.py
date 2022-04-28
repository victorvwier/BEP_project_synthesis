from common.environment.environment import Environment
from common.tokens.abstract_tokens import Token, TransToken, BoolToken


class Settings:
    """Abstract settings class."""

    def __init__(self, domain: str, trans_tokens: list[TransToken], bool_tokens: list[BoolToken]):
        self.domain = domain
        self.trans_tokens = trans_tokens
        self.bool_tokens = bool_tokens

    def distance(self, inp: Environment, out: Environment) -> float:
        """Returns the settings between two given Environments."""
        raise NotImplementedError()
