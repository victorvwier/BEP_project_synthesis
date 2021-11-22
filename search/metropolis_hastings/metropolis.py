from typing import Tuple
from common_environment.abstract_tokens import Token
from interpreter.interpreter import Program
from parser.experiment import TestCase
from search.abstract_search import SearchAlgorithm


class MetropolisHasting(SearchAlgorithm):
    @staticmethod
    def search(test_case: TestCase, trans_tokens: set[Token], bool_tokens: set[Token]) -> Program:
        program: Program = Program([])
        return program     