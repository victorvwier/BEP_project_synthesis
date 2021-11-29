from common.tokens.abstract_tokens import Token
from common.interpreter import Program
from common.experiment import TestCase


class SearchAlgorithm:
    # Returns (program, best_loss, !solved)
    @staticmethod
    def search(test_case: TestCase, trans_tokens: 'set[Token]', bool_tokens: 'set[Token]') -> Program:
        raise NotImplementedError()