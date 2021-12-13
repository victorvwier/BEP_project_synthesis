import json

class ResultParser:
    def __init__(self, file):
        self.file = file

    def complexity_succesPercentage(self):
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                obj = json.JSONDecoder().decode(stripped_line)
                print(obj)


