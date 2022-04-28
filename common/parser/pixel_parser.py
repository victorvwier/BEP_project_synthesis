import ast
import re

from common.environment.pixel_environment import PixelEnvironment
from common.parser.parser import Parser


class PixelParser(Parser):

    def __init__(self):
        super().__init__(path_train="examples/e3-pixels/data/")

    def parse_environment(self, args: str):
        # _,_,4,6,[0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0]
        # px, py, w, h
        split = args.split(",")

        return PixelEnvironment(
            x=0 if split[0] == "_" else int(split[0]) - 1,
            y=0 if split[1] == "_" else int(split[1]) - 1,
            width=int(split[2]),
            height=int(split[3]),
            pixels=ast.literal_eval(re.search("([0-9]+|_),([0-9]+|_),[0-9]+,[0-9]+,(.*)", args).group(3))
        )