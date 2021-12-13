import random

from common.tokens.control_tokens import If, LoopWhile
from common.tokens.string_tokens import *


class Invent:

    def __init__(self, trans_tokens: list[TransToken], bool_tokens: list[BoolToken]):
        self._trans_tokens = trans_tokens
        self._bool_tokens = bool_tokens

        self._ifs = self._all_ifs()
        self._loops = self._all_loops()

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

    def _all_ifs(self) -> list[If]:
        res = []

        for cond in self._bool_tokens:
            if cond.__class__ in [NotAtEnd, NotAtStart, IsNotLetter, IsNotUppercase, IsNotLowercase, IsNotNumber, IsNotSpace]:
                continue

            for e1 in self._trans_tokens:
                for e2 in self._trans_tokens:
                    res.append(If(cond, [e1, e2], []))
                    res.append(If(cond, [], [e1, e2]))

                    # Ifs with equal branches don't make sense
                    if e1 == e2:
                        continue

                    res.append(If(cond, [e1], [e2]))

        return res

    def _all_loops(self):
        res = []

        for cond in self._bool_tokens:
            for lb in self._trans_tokens:
                if lb.__class__ not in [MakeLowercase, MakeUppercase]:
                    res.append(LoopWhile(cond, [lb]))

                for t1 in self._trans_tokens:
                    res.append(LoopWhile(cond, [lb, t1]))

                    for cond1 in self._bool_tokens:
                        if cond1.__class__ in [NotAtEnd, NotAtStart, IsNotLetter, IsNotUppercase, IsNotLowercase,
                                              IsNotNumber, IsNotSpace]:
                            continue

                        if lb == t1 or cond == cond1:
                            continue

                        res.append(LoopWhile(cond, [If(cond1, [lb], [t1])]))

        return res
