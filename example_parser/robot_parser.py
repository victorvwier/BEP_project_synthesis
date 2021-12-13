from common.environment import RobotEnvironment
from common.experiment import Example, TestCase
from example_parser.parser import Parser


class RobotParser(Parser):

    def __init__(self, path: str = None, result_folder_path: str = None):
        super().__init__(
            domain_name="robot",
            path=path or "examples/e1-robots/data/",
            result_folder_path=result_folder_path or "results/e1-robots/"
        )

    def _parse_file_lines(self, file_name: str, lines: 'list[str]') -> (list[Example], list[Example]):
        # gets first line and removes unneeded characters
        line = lines[0][4:-2]

        # split into input and output entry
        entries = line.split("w(")[1:]

        example = Example(
            RobotParser._parse_entry(entries[0]),
            RobotParser._parse_entry(entries[1]),
        )
        return [example], [example]

    @staticmethod
    def _parse_entry(entry: str) -> RobotEnvironment:
        # splits entry by ',' and casts all items to integers
        e = list(map(int, entry[:-2].split(',')))

        return RobotEnvironment(
            rx=e[0]-1, ry=e[1]-1,
            bx=e[2]-1, by=e[3]-1,
            holding=e[4],
            size=e[5],
        )

if __name__ == "__main__":
    res1 = RobotParser(path="../examples/e1-robots/data/").parse()
    n = 10
    for res in res1.test_cases:
        n -= 1
        if n == 0:
            break

        print(res.training_examples[0].input_environment)
        print(res.training_examples[0].output_environment)