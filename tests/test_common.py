from ..interpreter.interpreter import *
from ..pixel_environment.pixel_tokens import *

def test_test():
    p1 = Program([MoveRight(), Draw()])
    env1 = PixelEnvironment(1,0,0,[[False]])
    result = p1.interp(env1)
    assert result.pixels == [[1]]