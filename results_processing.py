import json

class ResultParser:
    def __init__(self, file):
        self.file = file

    def filter_result_fields(self, fields: list[str]):
        results = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                res = json.JSONDecoder().decode(stripped_line)
                result = []
                for f in fields:
                    if f in res:
                        result.append(res[f])
                results.append(result)

        return results

    def get_result(self):
        results = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                res = json.JSONDecoder().decode(stripped_line)
                results.append(res)
        return results







