from common.tokens.abstract_tokens import TransToken, BoolToken
from common.tokens.control_tokens import If, LoopWhile
from search.vlns.large_neighborhood_search.invent.invent import Invent


class StaticInvent(Invent):

    def setup(self, trans_tokens: list[TransToken], bool_tokens: list[BoolToken]):
        super().setup(trans_tokens, bool_tokens)
        self._ifs = self._all_ifs()
        self._loops = self._all_loops()

    def _all_ifs(self) -> list[If]:
        res = []

        for cond in self._bool_tokens:
            if str(cond.__class__).__contains__("Not"):
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
                for t1 in self._trans_tokens:
                    res.append(LoopWhile(cond, [lb, t1]))

                    for cond1 in self._bool_tokens:
                        if str(cond.__class__).__contains__("Not"):
                            continue

                        if lb == t1 or cond == cond1:
                            continue

                        res.append(LoopWhile(cond, [If(cond1, [lb], [t1])]))

        return res
