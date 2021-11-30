import time
from statistics import mean
from typing import List

from common.prorgam import Program
from common.tokens.abstract_tokens import Token
from common.experiment import Example
from search.search_result import SearchResult


class Search:
    """Abstract interface for a program synthesis search algorithm."""

    def __init__(self, time_limit_sec: float):
        self.time_limit_sec = time_limit_sec
        self._best_program = Program([])

    @property
    def best_program(self) -> Program:
        return self._best_program

    def setup(self, training_examples: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]):
        """This method is called before a search is performed. The search will be performed for the given 'test_case'. 
        Also the 'trans_tokens' and 'bool_tokens' that are available for the environment are given."""

        raise NotImplementedError()

    def iteration(self, training_example: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]) -> bool:
        """This method represents an iteration of the search algorithm. This method will get called over and over 
        again, as long as it returns True. It will stop whenever False is returned or a time limit is reached. The 
        search will be performed for the given 'test_case'. Also the 'trans_tokens' and 'bool_tokens' that are 
        available for the environment are given."""

        raise NotImplementedError()

    def extend_result(self, search_result: SearchResult):
        """The result of a search is stored a SearchResult object, containing a key-value dictionary. Whenever an
        algorithm needs to collect more data than is collected by default, one can append key-value pairs to the result.
        """

        return search_result

    def run(self, training_examples: List[Example], trans_tokens: set[Token], bool_tokens: set[Token]) -> SearchResult:
        """"Runs the search method until a program is returned or the time limit is reached. First the setup method is
        called, followed by a repetition of the iteration method until either a result is obtained, or the time limit is
        reached"""
        start_time = time.process_time()

        # Call setup.
        self.setup(training_examples, trans_tokens, bool_tokens)

        # self.iteration returns whether a new iteration should be performed. Break the loop if time limit reached.
        while self.iteration(training_examples, trans_tokens, bool_tokens):
            if time.process_time() >= start_time + self.time_limit_sec:
                break

        run_time = time.process_time() - start_time

        # Extend results and return.
        return self.extend_result(SearchResult(self.best_program, run_time))

    @staticmethod
    def cost_train(training_examples: List[Example], p: Program):
        return mean([p.interp(ex.input_environment).distance(ex.output_environment) for ex in training_examples])
