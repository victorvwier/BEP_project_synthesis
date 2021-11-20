from os import listdir

from parser.experiment import *


class Parser:
    """Abstract class implementing some helper methods for parsers."""

    def __init__(self, domain_name: str, path: str, result_folder_path: str, file_names: 'list[str]' = None):
        """Inits a new Parser given a domain name, path where train data is stored or a list of files to Parse."""
        self.domain_name = domain_name
        self.path = path
        self.result_folder_path = result_folder_path

        if file_names is None:
            self.file_names = listdir(path)
        else:
            self.file_names = file_names

    def _parse_file_lines(self, file_name: str, lines: 'list[str]') -> TestCase:
        """Parses given lines that are in a file, returns a TestCase."""
        raise NotImplementedError()

    def parse_file(self, file_name: str) -> TestCase:
        """Parses a file with a given file name found in the train data folder of the correct environment."""
        file = open(self.path + file_name, 'r')
        data = self._parse_file_lines(file_name, file.readlines())
        file.close()
        return data

    def parse_all(self, experiment_name: str = "unnamed_experiment", file_prefix: str = "") -> Experiment:
        """Parses all files with a given prefix. If none is given, parses all files."""
        files = self.file_names

        if file_prefix != "":
            files = list(filter(lambda x : x.startswith(file_prefix), self.file_names))

        if len(files) == 0:
            raise Exception("No files were found with prefix \"{}\" at path \"{}\".".format(file_prefix, self.path))

        return Experiment(
            experiment_name,
            self.domain_name,
            list(map(self.parse_file, files)),
        )

