from common.tokens.abstract_tokens import TransToken, BoolToken, InventedToken
from common.tokens.control_tokens import If, LoopWhile, LoopWhileThen
from solver.invent.invent import Invent


class StaticInvent(Invent):

    def setup(self, trans_tokens: list[TransToken], bool_tokens: list[BoolToken]):
        super().setup(trans_tokens, bool_tokens)
        self.ifs = self._all_ifs()
        self.loops = self._all_loops()
        self.perms = self._all_permutations()

    def _all_ifs(self) -> list[If]:
        res = []

        for cond in self._bool_tokens:
            if str(cond.__class__).__contains__("Not"):
                continue

            for e1 in self._trans_tokens:
                res.append(If(cond, [e1], []))

                for e2 in self._trans_tokens:
                    #res.append(If(cond, [e1, e2], []))
                    #res.append(If(cond, [], [e1, e2]))

                    # Ifs with equal branches don't make sense
                    if e1 == e2:
                        continue

                    res.append(If(cond, [e1], [e2]))

        return res

    def _all_loops(self):
        res = []

        #for cond in self._bool_tokens:
            #for lb in self._trans_tokens:
                #res.append(LoopWhileThen(cond, [lb], []))

        for cond in self._bool_tokens:
            for lb in self._trans_tokens:
                for t1 in self._trans_tokens:
                    res.append(LoopWhileThen(cond, [lb], [t1]))
                    #res.append(LoopWhileThen(cond, [lb, t1], []))

                    for cond1 in self._bool_tokens:
                        if str(cond.__class__).__contains__("Not"):
                            continue

                        if lb == t1 or cond == cond1:
                            continue

                        ##res.append(LoopWhileThen(cond, [If(cond1, [lb], [t1])], []))

        return res

    def _all_permutations(self):
        res = []

        for t1 in self._trans_tokens:
            res.append(InventedToken([t1]))

        for t1 in self._trans_tokens:
            for t2 in self._trans_tokens:
                res.append(InventedToken([t1, t2]))

        return res