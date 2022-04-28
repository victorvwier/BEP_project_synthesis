from dataclasses import dataclass


@dataclass(eq=True, unsafe_hash=True)
class Environment:
    """Abstract Environment class."""

    def correct(self, other: "Environment") -> bool:
        """Returns whether this state is the desired one given a desired output Environment."""
        raise NotImplementedError()

    def loop_limit(self) -> int:
        """Returns the max amount of loop iterations based on the environment."""
        raise NotImplementedError()

    def __lt__(self, other):
        return True

    def __deepcopy__(self, memdict={}):
        raise NotImplementedError()
