from common_environment.environment import PixelEnvironment
from myparser.experiment import Example, TestCase
from myparser.parser import Parser

class PixelParser(Parser):

    def __init__(self, path: str = None, result_folder_path: str = None):
        super().__init__(
            domain_name="pixel",
            path=path or "programs/e3-pixels/data/",
            result_folder_path=result_folder_path or "results/e3-pixels/"
        )

    def _parse_file_lines(self, file_name: str, lines: 'list[str]') -> TestCase:
        # get first line and remove unneeded characters.
        line = lines[0][4:-2]

        # splits into input and output
        entries = line.split("w(")[1:]
        
        example = Example(
            PixelParser._parse_entry(entries[0]),
            PixelParser._parse_entry(entries[1]),
        )

        return TestCase(
            path_to_result_file=self.result_folder_path + file_name,
            training_examples=[example],
            test_examples=[example]
        )

    @staticmethod
    def _parse_entry(entry: str) -> PixelEnvironment:
        # parses first four entries about position of pointer and width and height.
        e = list(map(
            PixelParser._parse_value,
            entry[:-2].split(',')[:4]
        ))

        # retries the actual array and split by ','
        arr = entry.split("[")[1].split("]")[0].split(",")

        # empty array
        pixels = [[] for i in range(e[2])]
        i = 0
        j = 0

        # fills up array
        for a in arr:
            if i == e[2]:
                i = 0

            pixels[i].append(a)
            i += 1

        return PixelEnvironment(
            x=e[0]-1, y=e[1]-1,
            width=e[2],
            height=e[3],
            pixels=pixels
        )

    @staticmethod
    def _parse_value(val: str) -> int:
        # casts to int if numeric, 0 otherwise.
        if val.isnumeric():
            return int(val)
        return 1

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