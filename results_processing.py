import json
from typing import Callable, List

from common.prorgam import Program

class ResultParser:
    def __init__(self, file):
        self.file = file

    def filter_result_fields(self, fields: List[str], successful=False):
        results = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                obj = json.JSONDecoder().decode(stripped_line)
                if(not successful or obj["test_cost"] == 0):
                    filtered = []
                    for f in fields:
                        if f in obj:
                            filtered.append(obj[f])
                    results.append(filtered)
                        
        return results

    def get_solved_count(self):
        solved, cases = 0,0
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                obj = json.JSONDecoder().decode(stripped_line)
                if(obj["train_cost"] == 0 and obj["test_cost"] == 0):
                    solved += 1
                cases += 1
                        
        return solved, cases
                            


