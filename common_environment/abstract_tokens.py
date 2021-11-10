from ..common_environment.environment import *

class Token:
    """Abstract Token. Enforces that all tokens have an apply method."""

    def apply(self, env: Environment):
        """Applies this Token on a given Environment."""
        raise NotImplementedError()

class BoolToken(Token):
    """Abstract Token that returns a boolean value."""

    def apply(self, env: Environment) -> bool:
        """Applies this BoolToken on a given Environment. Returns a boolean value."""
        raise NotImplementedError()

class TransToken(Token):
    """Abstract Token that can transform an Environment."""

    def apply(self, env: Environment) -> Environment:
        """Applies this TransToken on a given Environment. Alters the Environment and returns the newly obtained one."""

        raise NotImplementedError()

class ControlToken(Token):
    """Abstract Token used for flow control."""

    def apply(self, env: Environment) -> Environment:
        """Applies this ControlToken on a given Environment. Alters the Environment and returns the newly obtained one."""

        raise NotImplementedError()

class InventedToken(Token):
    def apply(self, env: Environment) -> Environment:
        raise NotImplementedError()

class InvalidTransition(Exception):
    """This exception will be raised whenever an invalid state transition is performed on an Environment."""
    pass