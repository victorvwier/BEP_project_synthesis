from common.settings.settings import Settings
from common.environment.robot_environment import RobotEnvironment
from common.tokens.robot_tokens import TransTokens, BoolTokens


class RobotGreedy(Settings):
    """A greedy settings measure for robot environment."""

    def __init__(self):
        super().__init__("robot", TransTokens, BoolTokens)

    def distance(self, inp: RobotEnvironment, out: RobotEnvironment) -> float:
        """Heuristic that was originally used by Brute."""

        return abs(inp.bx - out.bx) + abs(inp.by - out.by) \
               + abs(inp.rx - out.rx) + abs(inp.ry - out.ry) \
               + abs(int(inp.holding) - int(out.holding))