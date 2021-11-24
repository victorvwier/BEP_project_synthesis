from typing import Callable
from common_environment.abstract_tokens import Token
from interpreter.interpreter import Program
from parser.experiment import TestCase
from search.abstract_search import SearchAlgorithm
import random

class MetropolisHasting(SearchAlgorithm):
    @staticmethod
    def search(test_case: TestCase, trans_tokens: set[Token], bool_tokens: set[Token]) -> Program:
        program: Program = Program([])
        for i in range(0, 100):
            Mutation("Generate random token", )
            return program



class Mutation():
    def __init__(self, name: str, fun: Callable[[Program], Program], probability: int):
        self.name = name
        self.fun : Callable[[Program], Program] = fun
        self.probability = probability

    def apply(self, program: Program) -> Program:
        return self.fun(program)
