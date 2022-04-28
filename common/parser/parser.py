import re
from pathlib import Path

from common.experiment import TestCase, Example


class Parser:

    def __init__(self, path_train: str, path_test: str = ""):

        self.path_train = Path(__file__).parent.parent.parent.joinpath(path_train)
        self.path_test = "" if path_test == "" else Path(__file__).parent.parent.parent.joinpath(path_test)

    def parse_environment(self, args: str):
        raise NotImplementedError()

    def _parse_file(self, complexity: int, task: int, trial: int, train: bool = True) -> list[Example]:
        file_name = "{}-{}-{}.pl".format(complexity, task, trial)
        path = self.path_train if train else self.path_test
        file = open(path.joinpath(file_name), 'r')
        lines = file.readlines()
        file.close()

        examples = []

        for line in lines:
            res = re.search("pos\(w\((.*)\),w\((.*)\)\).", line)

            inp = self.parse_environment(res.group(1))
            out = self.parse_environment(res.group(2))

            examples.append(Example(inp, out))

        return examples

    def parse_test_cases(self, cases: list[tuple]) -> list[TestCase]:
        res = []

        for co, ta, tr in cases:
            try:
                train = self._parse_file(co, ta, tr)
                test = train if self.path_test == "" else self._parse_file(co, ta, tr, False)

                res.append(TestCase(
                    training_examples=train,
                    test_examples=test,
                    index=(co, ta, tr),
                ))
            except FileNotFoundError:
                continue

        return res
