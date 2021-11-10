from common_environment.abstract_tokens import *
from common_environment.environment import *

"""
		BooleanTokens
"""


class AtEnd(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return env.pos == len(env.string) - 1


class AtStart(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return env.pos == 0


class IsLetter(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return env.string[env.pos].isalpha()


class IsNotLetter(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return not env.string[env.pos].isalpha()


class IsUppercase(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return env.string[env.pos].isupper()


class IsNotUppercase(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return not env.string[env.pos].isupper()


class IsLowercase(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return env.string[env.pos].islower()


class IsNotLowercase(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return not env.string[env.pos].islower()


class IsNumber(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return env.string[env.pos].isnumeric()


class IsNotNumber(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return not env.string[env.pos].isnumeric()


class IsSpace(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return env.string[env.pos].isnumeric()


class IsNotSpace(BoolToken):
    def apply(self, env: StringEnvironment) -> bool:
        return not env.string[env.pos].isnumeric()


"""
		TransTokens

"""


class MoveRight(TransToken):
    def apply(self, env: StringEnvironment) -> StringEnvironment:
        if env.pos == len(env.string) - 1:
            raise InvalidTransition()
        env.pos += 1

        return env


class MoveLeft(TransToken):
    def apply(self, env: StringEnvironment) -> StringEnvironment:
        if env.pos == 0:
            raise InvalidTransition()
        env.pos -= 1

        return env


class MakeUppercase(TransToken):
    def apply(self, env: StringEnvironment) -> StringEnvironment:
        env.string[env.pos] = env.string[env.pos].upper()

        return env


class MakeLowercase(TransToken):
    def apply(self, env: StringEnvironment) -> StringEnvironment:
        env.string[env.pos] = env.string[env.pos].lower()

        return env


class Drop(TransToken):
    def apply(self, env: StringEnvironment) -> StringEnvironment:
        nstr = env.string
        i = env.pos

        env.string = nstr[0:i:] + nstr[i + 1::]

        return env
