from pathlib import Path
from typing import Iterable

from common.experiment import *


class Parser:
    """Abstract class implementing some helper methods for parsers."""

    def __init__(self, domain_name: str, path: str, result_folder_path: str, file_names: 'list[str]' = None):
        """Inits a new Parser given a domain name, path where train data is stored or a list of files to Parse."""
        path = Path(__file__).parent.parent.joinpath(path)
        self.domain_name = domain_name
        self.path = path
        self.result_folder_path = result_folder_path
        self.file_names = file_names or [p.name for p in list(path.iterdir())]

    def _parse_file_lines(self, file_name: str, lines: 'list[str]') -> TestCase:
        """Parses given lines that are in a file, returns a TestCase."""
        raise NotImplementedError()

    def parse_file(self, file_name: str) -> TestCase:
        """Parses a file with a given file name found in the train data folder of the correct environment."""
        file = open(self.path.joinpath(file_name), 'r')
        data = self._parse_file_lines(file_name, file.readlines())
        file.close()
        return data

    def parse_all(self, experiment_name: str = "unnamed_experiment", file_prefix: str = "") -> Experiment:
        """Parses all files with a given prefix. If none is given, parses all files."""
        files = self.file_names

        if file_prefix != "":
            files = list(filter(lambda x: x.startswith(file_prefix), self.file_names))

        if len(files) == 0:
            raise Exception("No files were found with prefix \"{}\" at path \"{}\".".format(file_prefix, self.path))

        return Experiment(
            experiment_name,
            self.domain_name,
            list(map(self.parse_file, files)),
        )

    def parse_specific_range(self, task_size: Iterable, task_id: Iterable, trial_number: Iterable = range(1,10), experiment_name: str = "unnamed_experiment") -> Experiment:
        files = []

        for a in task_size:
            for b in task_id:
                for c in trial_number:
                    file_name = "{}-{}-{}.pl".format(a, b, c)
                    if(file_name in self.file_names):
                        files.append(file_name)

        if len(files) == 0:
            raise Exception("No files were found for the given ranges")
        
        return Experiment(
            experiment_name,
            self.domain_name,
            list(map(self.parse_file, files))
        )