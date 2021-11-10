from ..common_environment.environment import *

class Token:

    def apply(self, env: Environment):
        pass

class BoolToken(Token):
    def apply(self, env: Environment) -> bool:
        raise NotImplementedError()

class TransToken(Token):
    def apply(self, env: Environment) -> Environment:
        raise NotImplementedError()

class ControlToken(Token):
    pass

class InventedToken(Token):
    pass

class InvalidTransition(Exception):
    pass