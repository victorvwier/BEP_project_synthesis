from unittest import TestCase

from interpreter.interpreter import Program
from pixel_environment.pixel_tokens import *

class TestMoveRight(TestCase):
    def test_apply(self):
        p1 = Program([MoveRight(), Draw()])
        env1 = PixelEnvironment(2, 0, 0, [[False]])
        result = p1.interp(env1)
        print(result.pixels)
        assert result.pixels == [[1]]
