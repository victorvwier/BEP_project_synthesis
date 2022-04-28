from collections import Iterable
from itertools import chain

from common.experiment import TestCase
from common.parser.parser import Parser
from common.parser.pixel_parser import PixelParser
from common.parser.robot_parser import RobotParser
from common.parser.string_parser import StringParser


def get_test_cases(domain: str, files: (Iterable[int], Iterable[int], Iterable[int]), exclude: list[tuple]) -> list[TestCase]:
    files = _get_iterables(domain, files)
    parser = _get_parser(domain)

    res = []

    for co in files[0]:
        for ta in files[1]:
            for tr in files[2]:
                if not (co, ta, tr) in exclude:
                    res.append((co, ta, tr))

    return parser.parse_test_cases(res)


def _get_iterables(domain: str, files: (Iterable[int], Iterable[int], Iterable[int])):
    if domain == "string":
        def_iter = range(1, 10), chain(range(1, 278), range(279, 328)), range(1, 10)
    elif domain == "robot":
        def_iter = [2, 4, 6, 8, 10], range(0, 10), range(0, 11)
    elif domain == "pixel":
        def_iter = [1, 2, 3, 4, 5], range(0, 10), range(1, 11)
    else:
        raise Exception()

    return (
        def_iter[0] if len(files[0]) == 0 else files[0],
        def_iter[1] if len(files[1]) == 0 else files[1],
        def_iter[2] if len(files[2]) == 0 else files[2]
    )


def _get_parser(domain: str) -> Parser:
    if domain == "string":
        return StringParser()
    elif domain == "robot":
        return RobotParser()
    elif domain == "pixel":
        return PixelParser()
    else:
        raise Exception()
