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
                print(obj)

                result = []

                for f in fields:
                    if f in obj:
                        result.append(self._field_parser(obj, f))

        return results

    def _field_parser(self, obj, field):
        if field == "complexity":
            return obj["file"].split("/")[1].split("-")[0]

        return obj[field]
