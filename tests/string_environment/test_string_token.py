from unittest import TestCase

from interpreter.interpreter import Program
from string_environment.string_tokens import *


class TestStringTransTokens(TestCase):
    def test_move_right(self):
        p = Program([MoveRight()])
        env = StringEnvironment("string")

        res = p.interp(env)

        assert res.pos == 1
