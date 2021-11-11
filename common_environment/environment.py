from typing import get_type_hints


class Environment:
    """Abstract Environment class."""

    def __init__(self):
        self.program = None

    def distance(self, other: "Environment") -> float:
        """Returns the distance from this Environment to some other object."""
        raise NotImplementedError()

class RobotEnvironment(Environment):
    """Environment for the robot. A robot lives on a square matrix in which it needs to pick up a ball lying somewhere in that same matrix."""

    def __init__(self, size: int, rx: int, ry: int, bx: int, by: int, holding = False):
        """Creates new RobotEnvironment given a size, initial position of the robot (rx, ry), position of the ball (bx, by) and whether the robot is holding the ball."""
        self.size = size
        self.rx = rx
        self.ry = ry
        self.bx = bx
        self.by = by
        self.holding = holding

    def __str__(self):
        return "RobotEnvironment(Robot: (%s, %s), Bal: (%s, %s), Holding: %s)" % \
               (self.rx, self.ry, self.bx, self.by, self.holding)


class StringEnvironment(Environment):
    """Environment for string manipulation."""
    def __init__(self, string: str, pos: int = 0):
        """Creates new StringEnvironment given an initial string and a starting position of the pointer, 0 by default."""
        # Manipulating strings as a list of characters is more efficient.
        self._string = list(string)
        self.pos = pos

    def toString(self) -> str:
        return "".join(self._string)

    def _levenshtein(self, a: str, b: str, i: int, j: int):
        """Calculates Levenshtein distance between two string; the amount of changes (add, remove, alter characters) that need to be made to transform one into the other."""
        if i == 0:
            return j
        if j == 0:
            return i
        return min(
            self._levenshtein(a, b, i - 1, j) + 1,
            self._levenshtein(a, b, i, j - 1) + 1,
            self._levenshtein(a, b, i - 1, j - 1) + (1 if a[i] == a[j] else 0)
        )

    def distance(self, other: "StringEnvironment"):
        return self._levenshtein(self.string(), other.string(), len(self._string) - 1, len(other._string) - 1)


class PixelEnvironment(Environment):
    def __init__(self, width, height, x, y, pixels=None):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.pixels = pixels
        if not pixels:
            self.pixels = [[False for _ in range(height)] for _ in range(width)]

    def __str__(self):
        return "PixelEnvironment((%s, %s), %s)" % (self.x, self.y, self.pixels)
