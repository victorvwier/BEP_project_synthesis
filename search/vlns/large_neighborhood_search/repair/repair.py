from common.prorgam import Program
from common.tokens.abstract_tokens import EnvToken


class Repair:
    """Interface for repair methods."""

    def __init__(self):
        self.invent = None

    def repair(self, seqs: list[list[EnvToken]]) -> Program:
        """Repairs a given list of subsequences. Returns repaired Program."""

        raise NotImplementedError()

    def random_token(self, w_trans: float, w_if: float, w_loop: float) -> EnvToken:
        return self.invent.random_token(w_trans=w_trans, w_if=w_if, w_loop=w_loop)

    def reset(self):
        pass

    def increment_search_depth(self):
        pass
