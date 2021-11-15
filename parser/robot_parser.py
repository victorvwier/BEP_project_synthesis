from common_environment.environment import RobotEnvironment
from parser.experiment import Example, TestCase
from parser.parser import Parser


class RobotParser(Parser):

    def __init__(self, path: str = None, result_folder_path: str = None):
        super().__init__(
            domain_name="robot",
            path=path or "programs/e1-robots/data/",
            result_folder_path=result_folder_path or "results/e1-robots/"
        )

    def _parse_file_lines(self, file_name: str, lines: 'list[str]') -> TestCase:
        # gets first line and removes unneeded characters
        line = lines[0][4:-2]

        # split into input and output entry
        entries = line.split("w(")[1:]

        example = Example(
            RobotParser._parse_entry(entries[0]),
            RobotParser._parse_entry(entries[1]),
        )
        return TestCase(
            path_to_result_file=self.result_folder_path + file_name,
            training_examples=[example],
            test_examples=[example]
        )

    @staticmethod
    def _parse_entry(entry: str) -> RobotEnvironment:
        # splits entry by ',' and casts all items to integers
        e = list(map(int, entry[:-2].split(',')))

        return RobotEnvironment(
            rx=e[0], ry=e[1],
            bx=e[2], by=e[3],
            holding=e[4],
            size=e[5],
        )

if __name__ == "__main__":
    res1 = RobotParser(path="../programs/e1-robots/data/").parse()
    n = 10
    for res in res1.test_cases:
        n -= 1
        if n == 0:
            break

        print(res.training_examples[0].input_environment)
        print(res.training_examples[0].output_environment)