import re
from dataclasses import dataclass

from common.environment.environment import Environment


@dataclass(eq=True)
class PixelEnvironment(Environment):
    def __init__(self, width, height, x, y, pixels=None):
        assert 0 <= x < width
        assert 0 <= y < height

        super().__init__()

        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.pixels = pixels or tuple(False for _ in range(width * height))

    def loop_limit(self) -> int:
        return max(self.width, self.height)

    def __hash__(self):
        return hash(("".join([str(p) for p in self.pixels]), self.x, self.y))

    def __deepcopy__(self, memdict={}):
        return PixelEnvironment(self.width, self.height, self.x, self.y, self.pixels)

    def __str__(self):
        return "PixelEnvironment((%s, %s), %s)" % (self.x, self.y, self.pixels)
