import random

from common_environment.control_tokens import If, LoopWhile
from interpreter.interpreter import Program, EnvToken, Token
from vlns.large_neighborhood_search.implementations.greedy_lns.destroyed_tokens import DestroyedEnvToken, DestroyedBoolToken
from vlns.large_neighborhood_search.repair import Repair


class ProbabilisticProgramRepair(Repair[Program]):

    def __init__(self, p_remove: float, p_split: float, domain: str):
        """Initializes a new probabilistic program repair method. Each destroyed token is replaced by a random suitable
        token from 'env_token_library' or 'bool_token_library'. With a chance of `p_remove` the entire token is
        removed. With a chance of `p_split` two tokens will be added."""
        super().__init__(domain)

        assert 0 <= p_remove <= 1
        assert 0 <= p_split <= 1

        self.p_remove = p_remove
        self.p_split = p_split

    def _init_random(self, token_classes, call = True):
        if call:
            return random.sample(token_classes, 1)[0]()
        else:
            return random.sample(token_classes, 1)[0]

    def repair(self, destroyed_solution: Program) -> Program:
        if len(destroyed_solution.sequence) == 0:
            return Program([self._init_random(self.env_tokens)])

        return Program(self._repair_sequence(destroyed_solution.sequence))

    def _repair_sequence(self, tokens: list[Token]) -> list[EnvToken]:
        # Repairs an entire sequence of Tokens.
        repaired_seq = []

        for t in tokens:
            if isinstance(t, DestroyedEnvToken):
                # When not removing append token
                if random.random() >= self.p_remove:
                    repaired_seq.append(self._init_random(self.env_tokens))

                # When splitting append extra random token
                if random.random() < self.p_split:
                    repaired_seq.append(self._init_random(self.env_tokens))

            elif isinstance(t, If):
                repaired_seq.append(self._repair_if(t))
            elif isinstance(t, LoopWhile):
                repaired_seq.append(self._repair_loop(t))
            else:
                repaired_seq.append(t)

        return repaired_seq

    def _repair_if(self, token: If) -> If:
        # If cond destroyed pick random, otherwise don't change
        if isinstance(token.cond, DestroyedBoolToken):
            token.cond = self._init_random(self.bool_tokens)
        token.e1 = self._repair_sequence(token.e1)
        token.e2 = self._repair_sequence(token.e2)

        return token

    def _repair_loop(self, token: LoopWhile) -> LoopWhile:
        # If cond destroyed pick random, otherwise don't change
        if isinstance(token.cond, DestroyedBoolToken):
            token.cond = self._init_random(self.bool_tokens)
        token.loop_body = self._repair_sequence(token.loop_body)

        return token


class StochasticProgramRepair(ProbabilisticProgramRepair):

    def __init__(self, p_remove: float, p_split: float, iterations: int, domain: str):
        super().__init__(p_remove, p_split, domain)

        self.iterations = iterations

    def repair(self, destroyed_solution: Program) -> Program:
        if len(destroyed_solution.sequence) == 0:
            return Program([random.choice(self.env_tokens)])

        return Program(self._inner_repair(destroyed_solution.sequence))

    def _inner_repair(self, tokens: list[EnvToken]) -> list[EnvToken]:
        # Repairs an entire sequence of Tokens.
        repaired_seq = []

        i = 0
        while i < len(tokens):
            t = tokens[i]

            if isinstance(t, DestroyedEnvToken):
                # When not removing append token
                if random.random() >= self.p_remove:
                    repaired_seq.append(self._find_stochastic_token(tokens, i))
                    i += 1
                # When splitting append extra random token
                if random.random() < self.p_split:
                    repaired_seq.append(self._find_stochastic_token(tokens, i))
                    i += 1
            elif isinstance(t, If):
                repaired_seq.append(self._repair_if(t))
                i += 1
            elif isinstance(t, LoopWhile):
                repaired_seq.append(self._repair_loop(t))
                i += 1
            else:
                repaired_seq.append(t)
                i += 1

        return repaired_seq

    def _find_stochastic_token(self, tokens: list[EnvToken], index: int) -> Token:
        lowest = (float('inf'), None)

        for t in self.env_tokens:
            loss = 0

            for _ in range(self.iterations):
                tokens_copy = copy.deepcopy(tokens)
                tokens_copy[index] = t

                p = Program(tokens_copy)
                loss += self.cost(p)

            if loss < lowest[0]:
                lowest = (loss, t)

        return lowest[1]