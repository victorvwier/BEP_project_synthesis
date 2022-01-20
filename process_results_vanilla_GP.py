import json
import statistics
from typing import Callable, List

from common.prorgam import Program

class ResultParser:
    def __init__(self, file):
        self.file = file

    def filter_result_fields(self, chosen_fields):
        results = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)
                filtered = []
                for f in chosen_fields:
                    if f in data:
                        filtered.append(data[f])
                results.append(filtered)
        return results

    def get_solved_count(self):
        solved, cases = 0, 0
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)
                if(data["train_cost"] == 0 and data["test_cost"] == 0):
                    solved += 1
                cases += 1
        return solved, cases

    def get_percentage_solved(self):
        solved, cases = self.get_solved_count()
        return str((solved / cases ) * 100) + "%"

    def relative_improvement(self):
        rel_improvement_all_files = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"]
                initial_cost = data["initial_cost"]
                final_cost = data["train_cost"]
                rel_improvement = ((initial_cost - final_cost) / initial_cost) * 100.0
                rel_improvement_all_files.append((file_name, rel_improvement))
        return rel_improvement_all_files

    def rate_of_improvement(self):
        rate = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"]
                initial_cost = data["initial_cost"]
                final_cost = data["train_cost"]
                time = data["number_of_explored_programs"]
                rel_improvement = ((initial_cost - final_cost) / initial_cost) * 100.0
                rate.append(rel_improvement / time)
                rate.append((file_name, rate))
        return rate

    def get_train_vs_test_cost(self):
        return self.filter_result_fields(["train_cost", "test_cost"])

    def improvement_over_iterations(self):

        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)
                costs = data["cost_per_iteration"]

                mx_my = [list(entry) for entry in zip(*costs)]
                mx = mx_my[0]
                my = mx_my[1]

                print(mx)
                print(my)


# Initialization
file_name_pixel = "gp-20220117-003706.txt"
file_name_robot = "gp-20220116-235934.txt"
file_name_string = "gp-20220117-000604.txt"

path_to_file_pixel = "./results/pixel/" + file_name_pixel
path_to_file_robot = "./results/robot/" + file_name_robot
path_to_file_string = "./results/string/" + file_name_string

result_parser_pixel = ResultParser(path_to_file_pixel)
result_parser_robot = ResultParser(path_to_file_robot)
result_parser_string = ResultParser(path_to_file_string)

# Processing
print(result_parser_pixel.get_percentage_solved())
print(result_parser_robot.get_percentage_solved())
print(result_parser_string.get_percentage_solved())
print(result_parser_string.get_train_vs_test_cost())

# Visualization
