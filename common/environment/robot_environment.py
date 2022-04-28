import re
from dataclasses import dataclass

from common.environment.environment import Environment


@dataclass(eq=True)
class RobotEnvironment(Environment):
    """Environment for the robot. A robot lives on a square matrix in which it needs to pick up a ball lying somewhere
    in that same matrix."""

    size: int
    rx: int
    ry: int
    bx: int
    by: int
    holding: bool

    def __init__(self, size: int, rx: int, ry: int, bx: int, by: int, holding=False):
        """Creates new RobotEnvironment given a size, initial position of the robot (rx, ry), position of the ball
        (bx, by) and whether the robot is holding the ball."""
        assert (not holding or (rx == bx and ry == by))
        super().__init__()

        self.size = size
        self.rx = rx
        self.ry = ry
        self.bx = bx
        self.by = by
        self.holding = holding

    def loop_limit(self) -> int:
        return self.size

    def __hash__(self):
        return hash((self.rx, self.ry, self.bx, self.by, self.holding, self.size))

    def __deepcopy__(self, memdict={}):
        return RobotEnvironment(self.size, self.rx, self.ry, self.bx, self.by, self.holding)

    def __str__(self):
        return "RobotEnvironment(Robot: (%s, %s), Bal: (%s, %s), Holding: %s, Size: %s)" % \
               (self.rx, self.ry, self.bx, self.by, self.holding, self.size)
