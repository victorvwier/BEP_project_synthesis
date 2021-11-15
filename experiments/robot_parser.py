from common_environment.environment import RobotEnvironment
from experiments.experiment import Example, TestCase
from experiments.parser import Parser


class RobotParser(Parser):

    def __init__(self, path: str = None):
        super().__init__(
            domain_name="robot",
            path=path or "../programs/e1-robots/data/",
        )

    def _parse_file_lines(self, file_name: str, lines: list[str]) -> TestCase:
        line = lines[0][4:-2]
        entries = line.split("w(")[1:]

        example = Example(
            RobotParser._parse_entry(entries[0]),
            RobotParser._parse_entry(entries[1]),
        )
        return TestCase(
            file_name=file_name,
            training_examples=[example],
            test_examples=[]
        )

    @staticmethod
    def _parse_entry(entry: str) -> RobotEnvironment:
        e = list(map(int, entry[:-2].split(',')))

        return RobotEnvironment(
            rx=e[0], ry=e[1],
            bx=e[2], by=e[3],
            holding=e[4],
            size=e[5],
        )

if __name__ == "__main__":
    res1 = RobotParser().parse()
    n = 10
    for res in res1.test_cases:
        n -= 1
        if n == 0:
            break

        print(res.training_examples[0].input_environment)
        print(res.training_examples[0].output_environment)