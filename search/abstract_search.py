from typing import Tuple
from common_environment.abstract_tokens import Token
from interpreter.interpreter import Program
from parser.experiment import TestCase


class SearchAlgorithm:
    """Abstract Token used for flow control."""
    # Returns (program, best_loss, !solved)
    def search(test_case: TestCase, trans_tokens: set[Token], bool_tokens: set[Token]) -> Tuple[Program, int, int]:
        """Applies this ControlToken on a given Environment. Alters the Environment and returns the newly obtained one."""

        raise NotImplementedError()