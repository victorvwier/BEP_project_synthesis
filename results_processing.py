import json
from typing import Callable, List

from common.prorgam import Program

class ResultParser:
    def __init__(self, file):
        self.file = file

    def filter_result_fields(self, fields: List[str]):
        results = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                obj = json.JSONDecoder().decode(stripped_line)
                for res in obj['results']:
                    result = []
                    for f in fields:
                        if f in res:
                            result.append(res[f])
                    results.append(result)

        return results
                            


