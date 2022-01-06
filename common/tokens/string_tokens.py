from common.tokens.abstract_tokens import *
from common.environment import *

#                           #
#       BoolTokens          #
#                           #


class AtEnd(BoolToken):
    """Token that returns whether the pointer is at the end of the string."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return env.pos == len(env.string_array) - 1


class NotAtEnd(BoolToken):
    """Token that returns whether the pointer is not at the end of the string."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return env.pos != len(env.string_array) - 1


class AtStart(BoolToken):
    """Token that returns whether the pointer is at the start of the string."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return env.pos == 0


class NotAtStart(BoolToken):
    """Token that returns whether the pointer is not at the start of the string."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return env.pos != 0


class IsLetter(BoolToken):
    """Token that returns whether the character at the pointers position is an alphabetical letter."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return env.string_array[env.pos].isalpha()


class IsNotLetter(BoolToken):
    """Token that returns whether the character at the pointers position is not an alphabetical letter."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return not env.string_array[env.pos].isalpha()


class IsUppercase(BoolToken):
    """Token that returns whether the character at the pointers position is in uppercase."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return env.string_array[env.pos].isupper()


class IsNotUppercase(BoolToken):
    """Token that returns whether the character at the pointers position is not in uppercase."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return not env.string_array[env.pos].isupper()


class IsLowercase(BoolToken):
    """Token that returns whether the character at the pointers position is in lowercase."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return env.string_array[env.pos].islower()


class IsNotLowercase(BoolToken):
    """Token that returns whether the character at the pointers position is not in lowercase."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return not env.string_array[env.pos].islower()


class IsNumber(BoolToken):
    """Token that returns whether the character at the pointers position is a number."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return env.string_array[env.pos].isnumeric()


class IsNotNumber(BoolToken):
    """Token that returns whether the character at the pointers position is not a number."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return not env.string_array[env.pos].isnumeric()


class IsSpace(BoolToken):
    """Token that returns whether the character at the pointers position is a space character."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return env.string_array[env.pos] == " "


class IsNotSpace(BoolToken):
    """Token that returns whether the character at the pointers position is not a space character."""

    def apply(self, env: StringEnvironment) -> bool:
        if len(env.string_array) == 0:
            raise InvalidTransition
        return not env.string_array[env.pos] == " "


#                           #
#       TransTokens         #
#                           #

class MoveRight(TransToken):
    """Token that moves the pointer one unit to the right. Raises InvalidTransition when the pointer moves out of the
    string."""

    def apply(self, env: StringEnvironment) -> StringEnvironment:
        if env.pos >= len(env.string_array) - 1:
            raise InvalidTransition()
        env.pos += 1

        return env


class MoveLeft(TransToken):
    """Token that moves the pointer one unit to the left. Raises InvalidTransition when the pointer moves out of the
    string."""

    def apply(self, env: StringEnvironment) -> StringEnvironment:
        if env.pos <= 0:
            raise InvalidTransition()
        env.pos -= 1

        return env


class MakeUppercase(TransToken):
    """Token that transforms the character at the pointers position into an uppercase character."""

    def apply(self, env: StringEnvironment) -> StringEnvironment:
        if len(env.string_array) == 0:
            raise InvalidTransition

        env.string_array[env.pos] = env.string_array[env.pos].upper()

        return env


class MakeLowercase(TransToken):
    """Token that transforms the character at the pointers position into a lowercase character."""

    def apply(self, env: StringEnvironment) -> StringEnvironment:
        if len(env.string_array) == 0:
            raise InvalidTransition

        env.string_array[env.pos] = env.string_array[env.pos].lower()

        return env


class Drop(TransToken):
    """Removes the character at the pointers position. If the last character is removed the pointer will be moved one
    to the left. If the string is empty an InvalidTransition exception will be raised."""

    def apply(self, env: StringEnvironment) -> StringEnvironment:
        if len(env.string_array) == 0:
            raise InvalidTransition

        #env.string_array = nstr[0:i] + nstr[i + 1:]
        del env.string_array[env.pos]

        env.pos = max(min(len(env.string_array) - 1, env.pos), 0)

        return env


BoolTokens = {AtEnd(), NotAtEnd(), AtStart(), NotAtStart(), IsLetter(), IsNotLetter(), IsUppercase(), IsNotUppercase(), IsLowercase(),
              IsNotLowercase(), IsNumber(), IsNotNumber(), IsSpace(), IsNotSpace()}
# TransTokens = {MoveRight(), MoveLeft(), MakeUppercase(), MakeLowercase(), Drop()}
TransTokens = {MoveLeft(), MoveRight(), MakeUppercase(), MakeLowercase(), Drop()}
