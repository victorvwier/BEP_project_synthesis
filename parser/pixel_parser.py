from common_environment.environment import PixelEnvironment
from parser.experiment import Example, TestCase
from parser.parser import Parser

class PixelParser(Parser):

    def __init__(self, path: str = None):
        super().__init__(
            domain_name="pixel",
            path=path or "programs/e3-pixels/data/",
        )

    def _parse_file_lines(self, file_name: str, lines: list[str]) -> TestCase:
        line = lines[0][4:-2]
        entries = line.split("w(")[1:]
        print(file_name)
        example = Example(
            PixelParser._parse_entry(entries[0]),
            PixelParser._parse_entry(entries[1]),
        )

        return TestCase(
            file_name=file_name,
            training_examples=[example],
            test_examples=[example]
        )

    @staticmethod
    def _parse_entry(entry: str) -> PixelEnvironment:
        e = list(map(
            PixelParser._parse_value,
            entry[:-2].split(',')[:4]
        ))

        arr = entry.split("[")[1].split("]")[0].split(",")

        pixels = [[] for i in range(e[2])]
        i = 0
        j = 0

        for a in arr:
            if i == e[3]:
                i = 0
                j += 1

            pixels[j].append(a)
            i += 1

        return PixelEnvironment(
            x=e[0], y=e[1],
            width=e[2],
            height=e[3],
            pixels=pixels
        )

    @staticmethod
    def _parse_value(val: str) -> int:
        if val.isnumeric():
            return int(val)
        return 0

if __name__ == "__main__":
    res1 = PixelParser(path="../programs/e3-pixels/data/").parse()
    n = 10
    for res in res1.test_cases:
        n -= 1
        if n == 0:
            break

        print(res.file_name)
        print(res.training_examples[0].input_environment)
        print(res.training_examples[0].output_environment)