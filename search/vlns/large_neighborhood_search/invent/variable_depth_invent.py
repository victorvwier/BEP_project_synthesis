import copy
import random

from common.tokens.abstract_tokens import TransToken, BoolToken, EnvToken, ControlToken
from common.tokens.control_tokens import If, LoopWhile
from common.tokens.string_tokens import MoveRight, AtEnd, NotAtEnd


class VariableDepthInvent:
    def __init__(self, trans_tokens: list[TransToken], bool_tokens: list[BoolToken], max_depth: int, max_control_tokens: int):
        self._trans_tokens = trans_tokens
        self._bool_tokens = bool_tokens
        self._max_depth = max_depth
        self._max_control_tokens = max_control_tokens

        self._depth = 2

        self._ifs = self._all_ifs(1, 1)
        self._loops = self._all_loops(1, 1)

    def increment_depth(self):
        if self._depth == self._max_depth:
            return

        self._depth += 1
        self._ifs.extend(self._all_ifs(self._depth, self._max_control_tokens))
        self._loops.extend(self._all_loops(self._depth, self._max_control_tokens))

    def random_token(self, w_trans: float, w_if: float, w_loop: float) -> EnvToken:
        return random.choices([
            self.random_trans_token,
            self.random_if_token,
            self.random_loop_token,
        ], [w_trans, w_if, w_loop], k=1)[0]()

    def random_trans_token(self) -> TransToken:
        return random.sample(self._trans_tokens, 1)[0]

    def random_if_token(self) -> If:
        return random.sample(self._ifs, 1)[0]

    def random_loop_token(self) -> LoopWhile:
        return random.sample(self._loops, 1)[0]

    def _all_ifs(self, n: int, control_tokens: int, full: bool = False) -> list[If]:
        if n == 0 or (n == 1 and full) or control_tokens == 0:
            return []

        res = []

        for cond in self._bool_tokens:
            if str(cond.__class__).__contains__("Not"):
                continue

            r = range(1, n-1) if full else range(0, n)

            for l_e1 in r:
                for e1 in self._seqs(l_e1, control_tokens - 1):
                    for e2 in self._seqs(n - l_e1, control_tokens - 1):
                        if e1 == e2:
                            continue

                        res.append(If(cond, e1, e2))

        return res

    def _all_loops(self, n: int, control_tokens: int) -> list[LoopWhile]:
        if n == 0 or control_tokens == 0:
            return []

        res = []

        for cond in self._bool_tokens:
            for lb in self._seqs(n, control_tokens - 1, require_full_ifs=True, allow_loop_head=False):
                if len(lb) == 0:
                    continue

                res.append(LoopWhile(cond, lb))

        return res

    def _seqs(self, n: int, control_tokens: int, require_full_ifs=False, allow_loop_head=True) -> list[list[EnvToken]]:
        if n == 0:
            return [[]]

        res = []
        # Head normal token
        tails = self._seqs(n - 1, control_tokens, require_full_ifs)
        res.extend([copy.copy(tail) + [t] for t in self._trans_tokens for tail in tails])

        if control_tokens == self._max_control_tokens:
            return res

        # Head if
        for l_tail in range(0, n):
            tails = self._seqs(l_tail, control_tokens, require_full_ifs)
            res.extend([copy.copy(tail) + [t] for t in self._all_ifs(n - l_tail, control_tokens, full=require_full_ifs) for tail in tails])

        if not allow_loop_head:
            return res

        # Head loop
        for l_tail in range(0, n):
            tails = self._seqs(l_tail, control_tokens, require_full_ifs)
            res.extend(
                [copy.copy(tail) + [t] for t in self._all_loops(n - l_tail, control_tokens) for tail in tails])

        return res

if __name__ == "__main__":
    vdi = VariableDepthInvent([MoveRight()]*5,[AtEnd()]*14, 5, 2)
    l = vdi._all_loops(n=3, control_tokens=2)

    #print(l)
    print(len(l))