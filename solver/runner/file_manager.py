import json
import os


class FileManager:

    def __init__(self, algo: str, settings: str, suffix: str):
        self.folder = "{}/results/{}".format(os.getcwd(), algo)
        self.file_name = "{}-{}{}.txt".format(algo, settings, suffix)
        self.path = "{}/{}".format(self.folder, self.file_name)

        # Create folder if not existing
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def finished_test_cases(self):
        test_cases = []

        try:
            with open(self.path, "r") as file:
                for line in file.readlines():
                    obj = json.loads(line[:-1])
                    test_cases.append((obj["complexity"], obj["task"], obj["trial"]))
        except FileNotFoundError:
            return []

        return test_cases

    def append_result(self, results: list[dict]):
        with open(self.path, "a") as file:
            for result in results:
                file.write(json.dumps(result))
                file.write("\n")
