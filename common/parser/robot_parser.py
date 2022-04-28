from common.environment.robot_environment import RobotEnvironment
from common.parser.parser import Parser


class RobotParser(Parser):

    def __init__(self):
        super().__init__(path_train="examples/e1-robots/data/")

    def parse_environment(self, args: str):
        #2,2,1,2,0,2 --> rx, ry, bx, by, h, s

        e = list(map(int, args.split(',')))

        return RobotEnvironment(
            rx=e[0] - 1, ry=e[1] - 1,
            bx=e[2] - 1, by=e[3] - 1,
            holding=e[4],
            size=e[5],
        )