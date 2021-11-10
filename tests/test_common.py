from interpreter.interpreter import Program
from pixel_environment.pixel_tokens import *


def test_test():
    print ("aa")
    p1 = Program([MoveRight(), Draw()])
    env1 = PixelEnvironment(1,0,0,[[False]])
    result = p1.interp(env1)
    print(result.pixels)
    assert result.pixels == [[0]]