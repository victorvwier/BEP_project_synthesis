class Environment:
    """Abstract Environment class."""

    def distance(self, other) -> float:
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


class StringEnvironment(Environment):
    def __init__(self, string: str, pos: int):
        self.string = string
        self.pos = pos

    def _levenshtein(self, a: str, b: str, i: int, j: int):
        if i == 0:
            return j
        if j == 0:
            return i
        return min(
            self._levenshtein(a, b, i - 1, j) + 1,
            self._levenshtein(a, b, i, j - 1) + 1,
            self._levenshtein(a, b, i - 1, j - 1) + (1 if a[i] == a[j] else 0)
        )

    def distance(self, other: str):
        return self._levenshtein(self.string, other, len(self.string) - 1, len(other) - 1)


class PixelEnvironment(Environment):
    def __init__(self, size, x, y, pixels):
        self.size = size
        self.x = x
        self.y = y
        self.pixels = pixels