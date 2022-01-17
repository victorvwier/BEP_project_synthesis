from unittest import TestCase

from common.environment import StringEnvironment
from search.batch_run import BatchRun
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n import RemoveNInsertN


class TestStringCanReach(TestCase):
    trues = [
        ("ABC", "ABC"),
        ("ABC", "AC"),
        ("ABC", "AB"),
        ("ABC", "C"),
        ("ABC", "abc"),
        ("ABC", "aBc"),
    ]

    falses = [
        ("AB", "ABC"),
        ("ABC", "BAC"),
        ("AbC", "Acb"),
    ]

    def test_trues(self):
        for ex in self.trues:
            inp = StringEnvironment(list(ex[0]))
            out = StringEnvironment(list(ex[1]))

            self.assertTrue(inp.can_reach(out))

    def test_falses(self):
        for ex in self.falses:
            inp = StringEnvironment(list(ex[0]))
            out = StringEnvironment(list(ex[1]))

    def test_list_unreachables(self):
        # Definitely unreachable string tasks: {98, 12, 273, 274, 276, 277, 25, 250, 95}
        # 98 is parsed wrong.
        br = BatchRun(
            domain="string",
            files=([9],[],[1]),
            search_algorithm=RemoveNInsertN(10),
            file_name="",
        )

        un = set()
        for tc in br.test_cases:
            inp = tc.training_examples[0].input_environment
            out = tc.training_examples[0].output_environment

            if not inp.can_reach(out):
                un.add(tc.index[1])
                print("{}: In: {}. Out: {}".format(tc.index[1], "".join(inp.string_array), "".join(out.string_array)))

        print(un)