import random
from collections import Set, Callable

from common.prorgam import Program, EnvToken, BoolToken, Token
from common.tokens.control_tokens import If, LoopWhile
from search.vlns.large_neighborhood_search.tokens.sequence_token import SeqToken, SequenceToken, EmptySequenceToken


class Repair:

    def __init__(self):
        self.env_tokens = set()
        self.env_tokens: Set[EnvToken]
        self.bool_tokens = set()
        self.bool_tokens: Set[BoolToken]

        self.cost: Callable[[SeqToken], float]
        self.cost = lambda p: -1

    def repair(self, destroyed: SeqToken) -> Program:
        """Repairs a given `destroyed_solution'. Returns the repaired solution."""
        if isinstance(destroyed, EmptySequenceToken):
            destroyed = SequenceToken(self.env_token_sample(1)[0], destroyed)

        return Program(self.repair_sequence(destroyed).to_list())

    def repair_sequence(self, destroyed: SequenceToken) -> SeqToken:
        raise NotImplementedError()

    def set_token_libraries(self, env_tokens: set[EnvToken], bool_tokens: set[BoolToken]):
        self.env_tokens = env_tokens
        self.bool_tokens = bool_tokens

    def env_token_sample(self, k: int) -> list[EnvToken]:
        return random.sample(self.env_tokens, min(k, len(self.env_tokens)))

    def bool_token_sample(self, k: int) -> list[BoolToken]:
        return random.sample(self.bool_tokens, min(k, len(self.bool_tokens)))

    def random_if_token(self) -> If:
        return If(
            self.bool_token_sample(1)[0],
            [SequenceToken(self.env_token_sample(1)[0], EmptySequenceToken())],
            [SequenceToken(self.env_token_sample(1)[0], EmptySequenceToken())])

    def random_loop_token(self) -> LoopWhile:
        return LoopWhile(
            self.bool_token_sample(1)[0],
            [SequenceToken(self.env_token_sample(1)[0], EmptySequenceToken())])
