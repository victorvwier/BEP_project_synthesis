import copy
import re
from dataclasses import dataclass

from common.environment.environment import Environment


@dataclass(eq=True)
class StringEnvironment(Environment):
    """Environment for string manipulation."""
    string_array: list[str]
    pos: int

    def __init__(self, string_array: list[str], pos: int = 0):
        """Creates new StringEnvironment given an initial string and starting position of the pointer, 0 by default."""
        assert 0 <= pos < len(string_array) or len(string_array) == 0
        super().__init__()

        # Manipulating strings as a list of characters is more efficient.
        self.string_array = string_array
        self.pos = pos

    def loop_limit(self) -> int:
        return max(self.pos, len(self.string_array) - self.pos)

    def __deepcopy__(self, memdict={}):
        return StringEnvironment(string_array=copy.copy(self.string_array), pos=self.pos)

    def __hash__(self):
        return hash(("".join(self.string_array), self.pos))

    def __str__(self):
        return "StringEnvironment(Pointer at {pos} in \"{string_array}\")".format(pos=self.pos,
                                                                                  string_array="".join(self.string_array))