from common_environment.abstract_tokens import *
from common_environment.environment import *


class AtTop(BoolToken):
    def apply(self, env: PixelEnvironment) -> bool:
        return env.y == 0

class AtBottom(BoolToken):
    def apply(self, env: PixelEnvironment) -> bool:
        return env.y == env.size - 1

class AtLeft(BoolToken):
    def apply(self, env: PixelEnvironment) -> bool:
        return env.x == 0

class AtRight(BoolToken):
    def apply(self, env: PixelEnvironment) -> bool:
        return env.x == env.size - 1

class Draw(TransToken):
    def apply(self, env: PixelEnvironment) -> PixelEnvironment:
        env.pixels[env.x][env.y] = True
        return env

class MoveRight(TransToken):
	def apply(self, env: PixelEnvironment) -> PixelEnvironment:
		if env.x == env.size - 1:
			raise InvalidTransition()
		env.x += 1
		return env

class MoveLeft(TransToken):
	def apply(self, env: PixelEnvironment) -> PixelEnvironment:
		if env.x == 0:
			raise InvalidTransition()
		env.x -= 1
		return env

class MoveUp(TransToken):
	def apply(self, env: PixelEnvironment) -> PixelEnvironment:
		if env.y == 0:
			raise InvalidTransition()
		env.y -= 1
		return env

class MoveDown(TransToken):
	def apply(self, env: PixelEnvironment) -> PixelEnvironment:
		if env.y == env.size - 1:
			raise InvalidTransition()
		env.y += 1
		return env

BoolTokens = {AtTop, AtBottom, AtLeft, AtRight}
TransTokens = {MoveRight, MoveDown, MoveLeft, MoveUp, Draw}
