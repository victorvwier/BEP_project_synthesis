import random
from pathlib import Path
from typing import Iterable

from common.experiment import *


class Parser:
    """Abstract class implementing some helper methods for parsers."""

    def __init__(self, domain_name: str, path: str, result_folder_path: str):
        """Inits a new Parser given a domain name, path where train data is stored or a list of files to Parse."""
        path = Path(__file__).parent.parent.joinpath(path)
        self.domain_name = domain_name
        self.path = path
        self.result_folder_path = result_folder_path
        self.file_names = [p.name for p in list(path.iterdir())]

    def _parse_file_lines(self, file_name: str, lines: 'list[str]') -> (list[Example], list[Example]):
        """Parses given lines that are in a file, returns a TestCase."""
        raise NotImplementedError()

    def parse_file(self, file_name: str) -> TestCase:
        """Parses a file with a given file name found in the train data folder of the correct environment."""
        file = open(self.path.joinpath(file_name), 'r')
        data = self._parse_file_lines(file_name, file.readlines())
        file.close()

        i = file_name[:-3].split("-")

        return TestCase(
            path_to_result_file=self.result_folder_path + file_name,
            training_examples=data[0],
            test_examples=data[1],
            index=(int(i[0]), int(i[1]), int(i[2]))
        )

    def parse_specific_range(self, i1: Iterable, i2: Iterable, i3: Iterable) -> list[TestCase]:
        res = []

        for fn in self.file_names:
            e = self._extract_file_name(fn)

            if (not any(True for _ in i1) or e[0] in i1) and \
                (not any(True for _ in i2) or e[1] in i2) and \
                not e[1] == 999999 and \
                (not any(True for _ in i3) or e[2] in i3):
                res.append(self.parse_file(fn))

        return sorted(res, key=lambda r: r.index)

    @staticmethod
    def _extract_file_name(s: str) -> (int, int, int):
        e = s[:-3].split("-")

        if e[1].startswith("b"):
            e[1] = "999999"

        return int(e[0]), int(e[1]), int(e[2])
