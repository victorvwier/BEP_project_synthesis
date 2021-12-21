import copy
import random

from common.tokens.abstract_tokens import TransToken, BoolToken, EnvToken, ControlToken
from common.tokens.control_tokens import If, LoopWhile
from common.tokens.string_tokens import MoveRight, AtEnd, NotAtEnd
from search.vlns.large_neighborhood_search.invent.invent import Invent


class VariableDepthInvent(Invent):

    def __init__(self, depths: list[(int, int)]):
        super().__init__()

        self._depths = depths
        self._depth = -1

    def setup(self, trans_tokens: list[TransToken], bool_tokens: list[BoolToken]):
        super().setup(trans_tokens, bool_tokens)

        self._depth = -1
        self.increment_depth()

    def increment_depth(self):
        if self._depth == len(self._depths) - 1:
            return

        self._depth += 1

        d = self._depths[self._depth]

        self._ifs.extend(self._all_ifs(d[0], d[1]))
        self._loops.extend(self._all_loops(d[0], d[1]))

        print("Loops", len(self._loops))
        print("Ifs", len(self._ifs))

    def _all_ifs(self, n: int, control_tokens: int, full: bool = False) -> list[If]:
        if n == 0 or (n == 1 and full) or control_tokens == 0:
            return []

        res = []

        for cond in self._bool_tokens:
            if str(cond.__class__).__contains__("Not"):
                continue

            r = range(1, n) if full else range(0, n+1)

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

        if control_tokens == self._depths[self._depth][1]:
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
    vdi = VariableDepthInvent([(1, 1), (2, 1), (2, 2), (2, 3)])
    vdi.setup([MoveRight()], [AtEnd()])

    for i in range(4):
        if i > 0:
            vdi.increment_depth()

        ls = vdi._loops
        ifs = vdi._ifs

        print("Depth: {}".format(vdi._depths[vdi._depth]))
        print(len(ls), ls)
        print(len(ifs), ifs)