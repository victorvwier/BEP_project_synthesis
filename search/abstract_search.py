from typing import Tuple
from common_environment.abstract_tokens import Token
from interpreter.interpreter import Program
from parser.experiment import TestCase


class SearchAlgorithm:
    # Returns (program, best_loss, !solved)
    @staticmethod
    def search(test_case: TestCase, trans_tokens: 'set[Token]', bool_tokens: 'set[Token]') -> Program:
        raise NotImplementedError()