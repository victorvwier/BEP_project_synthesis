from common.experiment import Example
from common.tokens.abstract_tokens import TransToken, BoolToken
from search.brute.brute import Brute
from search.search_result import SearchResult
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n_vdi import RemoveNInsertNVDI


class FluteBruteVDI(RemoveNInsertNVDI):

    def __init__(self, inc_depth_after: int, time_limit_brute, time_limit_flute):
        super().__init__(inc_depth_after, time_limit_brute + time_limit_flute)

        self.time_limit_brute = time_limit_brute
        self.time_limit_flute = time_limit_flute

        self.brute = Brute(time_limit_brute)
        self.brute_time = 0

    def setup(self, test_case: list[Example], trans_tokens: list[TransToken], bool_tokens: list[BoolToken]):
        brute_res = self.brute.run(test_case, trans_tokens,  bool_tokens)
        brute_prog = brute_res.dictionary["program"]
        self.brute_time = brute_res.dictionary["execution_time"]

        self._best_program = brute_prog
        self.sol_current = brute_prog
        self.cost_best = self.cost(exs=test_case, p=self._best_program)
        self.cost_current = self.cost_best

        super().setup(test_case, trans_tokens, bool_tokens)

    def extend_result(self, res: SearchResult) -> SearchResult:
        res.dictionary["execution_time"] -= self.brute_time

        return res
