import re
import ast

from common.environment.string_environment import StringEnvironment
from common.parser.parser import Parser


class StringParser(Parser):

    def __init__(self):
        super().__init__(
            path_train="examples/e2-strings/data/train/",
            path_test="examples/e2-strings/data/test/"
        )

    def parse_environment(self, args: str):
        pos = args.split(",")[0]
        pos = 0 if pos == "_" else int(pos) - 1

        return StringEnvironment(
            string_array=ast.literal_eval(re.search("([0-9]+|_),[0-9]+,(.*)", args).group(2)),
            pos=pos
        )
