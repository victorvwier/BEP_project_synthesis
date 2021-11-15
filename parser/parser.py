from os import listdir

from parser.experiment import *


class Parser:

    def __init__(self, domain_name: str, path: str, file_names: list[str] = None):
        self.domain_name = domain_name
        self.path = path

        if file_names is None:
            self.file_names = listdir(path)
        else:
            self.file_names = file_names

    def _parse_file_lines(self, file_name: str, lines: list[str]) -> TestCase:
        raise NotImplementedError()

    def parse_file(self, file_name: str) -> TestCase:
        file = open(self.path + file_name, 'r')
        return self._parse_file_lines(file_name, file.readlines())

    def parse(self, experiment_name: str = "unnamed_experiment", file_prefix: str = "") -> Experiment:
        files = self.file_names

        if file_prefix != "":
            files = filter(lambda x : x.startswith(file_prefix), self.file_names)

        return Experiment(
            experiment_name,
            self.domain_name,
            list(map(self.parse_file, files)),
        )

