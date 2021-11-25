from common_environment.environment import StringEnvironment
from myparser.experiment import TestCase, Example
from myparser.parser import Parser


class StringParser(Parser):
    test_path = "programs/e2-strings/data/test/"

    def __init__(self, path: str = None, result_folder_path: str = None):
        super().__init__(
            domain_name="string",
            path=path or "programs/e2-strings/data/train/",
            result_folder_path=result_folder_path or "results/e2-strings/"
        )

    def _parse_file_lines(self, file_name: str, lines: 'list[str]') -> TestCase:
        test_lines = open(self.test_path + file_name, 'r').readlines()

        return TestCase(
            path_to_result_file=self.result_folder_path + file_name,
            training_examples=list(map(StringParser._parse_single_line, lines)),
            test_examples=list(map(StringParser._parse_single_line, test_lines))
        )

    @staticmethod
    def _parse_single_line(line: str) -> Example:
        # remove unneeded characters
        line = line[4:-1]

        # split input and output
        entries = line.split("w(")[1:]

        return Example(
            StringParser._parse_entry(entries[0]),
            StringParser._parse_entry(entries[1]),
        )

    @staticmethod
    def _parse_entry(entry: str) -> StringEnvironment:
        # first entry before ',' is pointer position.
        pos = entry.split(",")[0]

        # gets data between ',[' and '])' and picks every fourth character starting at index 1, which is the string.
        string = entry.split(",[")[1].split("])")[0][1::4]

        # for output data the position is not defined, however Environment needs one.
        if not pos.isnumeric():
            pos = 1

        return StringEnvironment(string, int(pos) - 1)

if __name__ == "__main__":
    p = StringParser(path="../programs/e2-strings/data/train/")
    p.test_path = "../programs/e2-strings/data/test/"

    res1 = StringParser().parse()

    for res in res1.test_cases:
        print(res.training_examples[0].input_environment.to_string())
        print(res.training_examples[0].output_environment.to_string())

        print(res.test_examples[0].input_environment.to_string())
        print(res.test_examples[0].output_environment.to_string())