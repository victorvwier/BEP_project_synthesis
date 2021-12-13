from typing import Union

from common.tokens.abstract_tokens import *
from common.prorgam import Program


class If(ControlToken):
    """If statement ControlToken."""

    def __init__(self, cond: BoolToken, e1: list[EnvToken], e2: list[EnvToken]):
        """Creates a new If ControlToken. When applied, 'cond' is executed. If that yields true, 'e1' is execute,
        otherwise 'e2'."""
        self.cond = cond
        self.e1 = e1
        self.e2 = e2

    def apply(self, env: Environment) -> Environment:
        if self.cond.apply(env):
            for token in self.e1:
                env = token.apply(env)
            return env
        for token in self.e2:
            env = token.apply(env)
        return env
        # Program(self.e2).interp(env, False)

    def number_of_tokens(self) -> int:
        return 1 + \
               sum([t.number_of_tokens() for t in self.e1]) + \
               sum([t.number_of_tokens() for t in self.e2])

    def __str__(self):
        return "If(%s [%s] [%s])" % (self.cond, ", ".join(list(map(str, self.e1))), ", ".join(list(map(str, self.e2))))

    def __repr__(self):
        return "If(%s [%s] [%s])" % (self.cond, ", ".join(list(map(str, self.e1))), ", ".join(list(map(str, self.e2))))

    def to_formatted_string(self):
        result = "if %s:\n\t%s" % (
            self.cond.to_formatted_string(),
            "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.e1])
        )
        if self.e2:
            result += "\nelse:\n\t%s" % (
                "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.e2])
            )
        return result


class LoopWhile(ControlToken):
    """Loop ControlToken."""

    def __init__(self, cond: BoolToken, loop_body: list[EnvToken]):
        """Creates a new Loop ControlToken. 'loop_body' will run as long as 'cond' is true."""
        self.cond = cond
        self.loop_body = loop_body

        self.input_map = {}

    def apply(self, env: Environment) -> Environment:
        # Raise exception if recursive call limit is reached
        # if the condition is None or true, make recursive call
        calls = 0
        limit = env.loop_limit()

        while self.cond.apply(env):
            if calls > limit:
                raise LoopIterationLimitReached()
            calls += 1

            for token in self.loop_body:
                token.apply(env)

        return env

    def number_of_tokens(self) -> int:
        return 1 + sum([t.number_of_tokens() for t in self.loop_body])

    def __str__(self):
        return "LoopWhile(%s [%s])" % \
               (self.cond, ", ".join(list(map(str, self.loop_body))))

    def __repr__(self):
        return "LoopWhile(%s [%s])" % \
               (self.cond, ", ".join(list(map(str, self.loop_body))))

    def to_formatted_string(self):
        result = "while %s do:\n\t%s" % (
            self.cond.to_formatted_string(),
            "\n\t".join([t.to_formatted_string().replace("\n", "\n\t") for t in self.loop_body])
        )
        return result


class LoopIterationLimitReached(Exception):
    """"Exception raised when the recursive call limit, set in the Program constructor is reached."""
    pass
