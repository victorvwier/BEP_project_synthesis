from common_environment.abstract_tokens import *
from common_environment.environment import *

class AtTop(BoolToken):
    def apply(self, env):
        assert isinstance(env, PixelEnvironment)
        return env.y == 0

class AtBottom(BoolToken):
    def apply(self, env):
        assert isinstance(env, PixelEnvironment)
        return env.y == env.size - 1

class AtLeft(BoolToken):
    def apply(self, env):
        assert isinstance(env, PixelEnvironment)
        return env.x == 0

class AtRight(BoolToken):
    def apply(self, env):
        assert isinstance(env, PixelEnvironment)
        return env.x == env.size - 1
