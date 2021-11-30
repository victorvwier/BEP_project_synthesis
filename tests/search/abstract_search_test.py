import math
import unittest

from common.experiment import TestCase
from common.prorgam import Program
from common.tokens.abstract_tokens import Token

from search.abstract_search import Search


class MySearch(Search):

    def __init__(self, max_iter: int, time_limit_sec: float):
        super().__init__(time_limit_sec)

        self.max_iter = max_iter

        self.iter_number = 1

    def setup(self, test_case: TestCase, trans_tokens: set[Token], bool_tokens: set[Token]):
        self.iter_number = 1
        self._best_program = Program([])

    def iteration(self, test_case: TestCase, trans_tokens: set[Token], bool_tokens: set[Token]) -> bool:
        self.iter_number += 1

        return self.iter_number <= self.max_iter


class MyTestCase(unittest.TestCase):
    def test_default(self):
        s = MySearch(10, 1)

        s.run(None, None, None)

        self.assertEqual(s.iter_number, 11)

    def test_timeout(self):
        s = MySearch(math.pow(10, 10), 1)

        r = s.run(None, None, None)

        self.assertEqual(len(s.best_program.sequence), 0)

        self.assertAlmostEqual(r.dictionary['execution_time'], 1, 5)


if __name__ == '__main__':
    unittest.main()
