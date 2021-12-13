from common.tokens.abstract_tokens import *
from common.environment import *


class AtTop(BoolToken):
	def apply(self, env: PixelEnvironment) -> bool:
		return env.y == 0


class AtBottom(BoolToken):
	def apply(self, env: PixelEnvironment) -> bool:
		return env.y == env.height - 1


class AtLeft(BoolToken):
	def apply(self, env: PixelEnvironment) -> bool:
		return env.x == 0


class AtRight(BoolToken):
	def apply(self, env: PixelEnvironment) -> bool:
		return env.x == env.width - 1


class NotAtTop(BoolToken):
	def apply(self, env: PixelEnvironment) -> bool:
		return env.y != 0


class NotAtBottom(BoolToken):
	def apply(self, env: PixelEnvironment) -> bool:
		return env.y != env.height - 1


class NotAtLeft(BoolToken):
	def apply(self, env: PixelEnvironment) -> bool:
		return env.x != 0


class NotAtRight(BoolToken):
	def apply(self, env: PixelEnvironment) -> bool:
		return env.x != env.width - 1


class Draw(TransToken):
	def apply(self, env: PixelEnvironment) -> PixelEnvironment:
		temp = list(env.pixels)
		temp[env.width * env.y + env.x] = True
		env.pixels = tuple(temp)
		return env


class Erase(TransToken):
	def apply(self, env: PixelEnvironment) -> PixelEnvironment:
		temp = list(env.pixels)
		temp[env.width * env.y + env.x] = False
		env.pixels = tuple(temp)
		return env


class MoveRight(TransToken):
	def apply(self, env: PixelEnvironment) -> PixelEnvironment:
		if env.x == env.width - 1:
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
		if env.y == env.height - 1:
			raise InvalidTransition()
		env.y += 1
		return env


BoolTokens = {AtTop, AtBottom, AtLeft, AtRight, NotAtTop, NotAtBottom, NotAtLeft, NotAtRight}
TransTokens = {MoveRight, MoveDown, MoveLeft, MoveUp, Draw, Erase}
