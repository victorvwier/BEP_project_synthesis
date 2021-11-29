import random
from typing import Callable, Iterable

from common_environment.abstract_tokens import *
from common_environment.control_tokens import LoopWhile, If
from experiment_procedure import extract_trans_tokens_from_domain_name, extract_bool_tokens_from_domain_name
from interpreter.interpreter import Program
from invent import invent2
from vlns.large_neighborhood_search.destroy.destroyed import DestroyedToken, DiscardToken
from vlns.large_neighborhood_search.implementations.wat_is_een_goeie_naam.marked_token import IdToken


class Repair:

    def __init__(self, domain: str, max_function_token_depth: int):
        self.env_tokens = extract_trans_tokens_from_domain_name(domain)
        self.bool_tokens = extract_bool_tokens_from_domain_name(domain)
        self.invented_tokens = invent2(self.env_tokens, self.bool_tokens, max_function_token_depth)

        self.cost: Callable[[Program], float]
        self.cost = lambda p: -1

        self.current_program = None
        self.current_cost = lambda: self.cost(self.current_program)

    def repair(self, destroyed_solution: list[EnvToken]) -> Program:
        """Repairs a given `destroyed_solution'. Returns the repaired solution."""

        self.current_program = Program(destroyed_solution)

        return Program(self._repair_sequence(destroyed_solution))

    def repair_destroyed_env(self, seq: list[EnvToken], token: Token, index: int) -> EnvToken:
        """In a given seq, the token at the given index is destroyed. This method returns the repaired token."""
        raise NotImplementedError()

    def repair_destroyed_bool(self, seq: list[EnvToken], control_token: ControlToken, index: int) -> BoolToken:
        """Whenever a BoolToken is destroyed this method gets called. The token that is returned will be the new
        BoolToken."""
        raise NotImplementedError()

    def _repair_sequence(self, seq: list[EnvToken]) -> list[EnvToken]:
        repaired_seq = []

        # For each index, token in seq
        for i, t in enumerate(seq):
            # When a destroyed token is found
            if isinstance(t, DestroyedToken):
                new_token = self.repair_destroyed_env(seq, t, i)

                if not isinstance(new_token, DiscardToken):
                    repaired_seq.append(self.repair_destroyed_env(seq, t, i))

            # IfToken found, subbranches need repairing
            elif isinstance(t, If):
                cond = self.repair_destroyed_bool(seq, t, i) if isinstance(t.cond, DestroyedToken) else t.cond
                e1 = self._repair_sequence(t.e1)
                e2 = self._repair_sequence(t.e2)

                repaired_seq.append(If(cond, e1, e2))

            # LoopWhile found, subbranch needs repairing
            elif isinstance(t, LoopWhile):
                cond = self.repair_destroyed_bool(seq, t, i) if isinstance(t.cond, DestroyedToken) else t.cond
                loop_body = self._repair_sequence(t.loop_body)

                repaired_seq.append(LoopWhile(cond, loop_body))

            # InventedToken found, inner sequence needs repairing
            elif isinstance(t, InventedToken):
                n_seq = self._repair_sequence(t.tokens)
                repaired_seq.append(InventedToken(n_seq))

            elif not isinstance(t, DiscardToken):
                repaired_seq.append(t)

        return repaired_seq

    def random_env(self, k: int) -> list[EnvToken]:
        return [t() for t in random.sample(self.env_tokens, min(k, len(self.env_tokens)))]

    def random_bool(self, k: int) -> list[BoolToken]:
        return [t() for t in random.sample(self.bool_tokens, min(k, len(self.bool_tokens)))]

    def random_invented(self, k: int):
        return random.sample(self.invented_tokens, min(k, len(self.invented_tokens)))
