from fileinput import filename
import json
import sys
from collections import OrderedDict

from matplotlib import pyplot as plt

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

    def solved_percentage_by_complexity(self, domain):
        solved_percentage = {}

        if (domain == "robot"):
            solved_percentage = {"2":[0, 0], "4":[0, 0], "6":[0, 0], "8":[0, 0], "10":[0, 0]}
        elif (domain == "string"):
            solved_percentage = {"1":[0, 0], "2":[0, 0], "3":[0, 0], "4":[0, 0], "5":[0, 0], "6":[0, 0], "7":[0, 0], "8":[0, 0], "9":[0, 0]}
        else:
            solved_percentage = {"1":[0, 0], "2":[0, 0], "3":[0, 0], "4":[0, 0], "5":[0, 0]}

        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"][len(domain)+2:]
                complexity = file_name.split('-')[0]

                if(data["train_cost"] == 0 and data["test_cost"] == 0):
                    solved_percentage[complexity][0] += 1
                solved_percentage[complexity][1] += 1

        for compl, (solved, total) in solved_percentage.items():
            if (total == 0):
                solved_percentage[compl] = 0
            else:
                solved_percentage[compl] = (solved / total) * 100

        return solved_percentage

    def rel_improvement_by_complexity(self, domain):
        rel_improvement = {}

        if (domain == "robot"):
            rel_improvement = {"2":[0, 0], "4":[0, 0], "6":[0, 0], "8":[0, 0], "10":[0, 0]}
        elif (domain == "string"):
            rel_improvement = {"1":[0, 0], "2":[0, 0], "3":[0, 0], "4":[0, 0], "5":[0, 0], "6":[0, 0], "7":[0, 0], "8":[0, 0], "9":[0, 0]}
        else:
            rel_improvement = {"1":[0, 0], "2":[0, 0], "3":[0, 0], "4":[0, 0], "5":[0, 0]}


        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"][len(domain)+2:]
                complexity = file_name.split('-')[0]

                initial_error = data["initial_error"]
                final_cost = data["train_cost"]

                if (initial_error == 0):
                    percentage_imp = 1
                else:
                    percentage_imp = (initial_error - final_cost) / initial_error

                rel_improvement[complexity][0] += percentage_imp
                rel_improvement[complexity][1] += 1

        for compl, [percent_sum, total_num] in rel_improvement.items():
            if (total_num == 0):
                rel_improvement[compl] = 0
            else:
                rel_improvement[compl] = (percent_sum / total_num) * 100

        return rel_improvement

#####################


    def get_solved_count_by_complexity(self, domain):
        solved_count = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"][len(domain)+2:]
                complexity = file_name.split('-')[0]

                if(data["train_cost"] == 0 and data["test_cost"] == 0):
                    solved_count.append((complexity, 1))

        solved_by_complexity = OrderedDict()
        for k, *v in solved_count:
            solved_by_complexity.setdefault(k, []).append(v)

        complexity_list = list(solved_by_complexity.items())
        solved_by_complexity = [(c, sum(sum(l_s, []))) for (c, l_s) in complexity_list]

        return solved_by_complexity


    def get_initial_error(self, example_name):
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"]

                if (file_name == example_name):
                    initial_error = data["initial_error"]
                    return initial_error


    def relative_improvement(self):
        rel_improvement_all_files = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"]
                
                initial_error = data["initial_error"]
                final_cost = data["train_cost"]
                if (initial_error == 0):
                    rel_improvement = 100.0
                else:
                   rel_improvement = ((initial_error - final_cost) / initial_error) * 100.0
                rel_improvement_all_files.append((file_name, rel_improvement))
        return rel_improvement_all_files

    def get_train_vs_test_cost(self):
        return self.filter_result_fields(["train_cost", "test_cost"])

    def error_progression(self, example_name):
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                if (data["file"] == example_name):
                    costs_per_iteration = data["cost_per_iteration"]
                    return costs_per_iteration

        

# Initialization
# VanillaGP
gp_file_name_pixel = sys.argv[1]
gp_file_name_robot = sys.argv[2]
gp_file_name_string = sys.argv[3]
gp_path_to_file_pixel = "./results/pixel/" + gp_file_name_pixel
gp_path_to_file_robot = "./results/robot/" + gp_file_name_robot
gp_path_to_file_string = "./results/string/" + gp_file_name_string

gp_result_parser_pixel = ResultParser(gp_path_to_file_pixel)
gp_result_parser_robot = ResultParser(gp_path_to_file_robot)
gp_result_parser_string = ResultParser(gp_path_to_file_string)

# Brute
brute_file_name_pixel = sys.argv[4]
brute_file_name_robot = sys.argv[5]
brute_file_name_string = sys.argv[6]
brute_path_to_file_pixel = "./results/pixel/" + brute_file_name_pixel
brute_path_to_file_robot = "./results/robot/" + brute_file_name_robot
brute_path_to_file_string = "./results/string/" + brute_file_name_string

brute_result_parser_pixel = ResultParser(brute_path_to_file_pixel)
brute_result_parser_robot = ResultParser(brute_path_to_file_robot)
brute_result_parser_string = ResultParser(brute_path_to_file_string)

# Processing
# print("Pixel, VanillaGP solved: ", gp_result_parser_pixel.get_percentage_solved())
# print("Robot, VanillaGP solved: ", gp_result_parser_robot.get_percentage_solved())
# print("String, VanillaGP solved: ", gp_result_parser_string.get_percentage_solved())

# print("Pixel, Brute solved: ", brute_result_parser_pixel.get_percentage_solved())
# print("Robot, Brute solved: ", brute_result_parser_robot.get_percentage_solved())
# print("String, Brute solved: ", brute_result_parser_string.get_percentage_solved())

def plot_error_progression(domain, example_name):
    initial_error = 0.0

    brute_cost_per_iteration = []
    if (domain == "pixel"):
        brute_cost_per_iteration = brute_result_parser_pixel.error_progression(example_name)
    elif (domain == "robot"):
        brute_cost_per_iteration = brute_result_parser_robot.error_progression(example_name)
    elif (domain == "string"):
        brute_cost_per_iteration = brute_result_parser_string.error_progression(example_name)

    gp_cost_per_iteration = []
    if (domain == "pixel"):
        initial_error = gp_result_parser_pixel.get_initial_error(example_name)
        gp_cost_per_iteration = gp_result_parser_pixel.error_progression(example_name)
    elif (domain == "robot"):
        initial_error = gp_result_parser_robot.get_initial_error(example_name)
        gp_cost_per_iteration = gp_result_parser_robot.error_progression(example_name)
    elif (domain == "string"):
        initial_error = gp_result_parser_string.get_initial_error(example_name)
        gp_cost_per_iteration = gp_result_parser_string.error_progression(example_name)

    initial_error_line = [(i, initial_error) for i in [*range(0, len(gp_cost_per_iteration))]]

    fig, ax = plt.subplots()
    ax.plot(*zip(*brute_cost_per_iteration[:len(gp_cost_per_iteration)]), label="Brute", color="red")
    ax.plot(*zip(*gp_cost_per_iteration), label="VanillaGP", color="blue")
    ax.plot(*zip(*initial_error_line), label="Initial Error", color="green")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Error")
    ax.legend()
    ax.set_title("Error Progression in Example {}".format(example_name))

    plt.savefig("plots/error_progression.svg")
    fig.clf()
    plt.close


def plot_complexity_vs_solved_percentage():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15,4))

    # Pixel
    domain = "pixel"
    brute_solved_percentage = brute_result_parser_pixel.solved_percentage_by_complexity(domain)
    gp_solved_percentage = gp_result_parser_pixel.solved_percentage_by_complexity(domain)
    ax1.plot(brute_solved_percentage.keys(), brute_solved_percentage.values(), label="Brute", color="red", marker="o")
    ax1.plot(gp_solved_percentage.keys(), gp_solved_percentage.values(), label="VanillaGP", color="blue", marker="o")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Tasks Solved (%)")
    ax1.legend()
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    brute_solved_percentage = brute_result_parser_robot.solved_percentage_by_complexity(domain)
    gp_solved_percentage = gp_result_parser_robot.solved_percentage_by_complexity(domain)
    ax2.plot(brute_solved_percentage.keys(), brute_solved_percentage.values(), label="Brute", color="red", marker="o")
    ax2.plot(gp_solved_percentage.keys(), gp_solved_percentage.values(), label="VanillaGP", color="blue", marker="o")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Tasks Solved (%)")
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    brute_solved_percentage = brute_result_parser_string.solved_percentage_by_complexity(domain)
    gp_solved_percentage = gp_result_parser_string.solved_percentage_by_complexity(domain)
    ax3.plot(brute_solved_percentage.keys(), brute_solved_percentage.values(), label="Brute", color="red", marker="o")
    ax3.plot(gp_solved_percentage.keys(), gp_solved_percentage.values(), label="VanillaGP", color="blue", marker="o")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Tasks Solved (%)")
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/solved_percentage.svg")
    fig.clf()
    plt.close

def plot_rel_improvement():
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15,4))

    # Pixel
    domain = "pixel"
    gp_avg_rel_improvement = gp_result_parser_pixel.rel_improvement_by_complexity(domain)
    ax1.plot(gp_avg_rel_improvement.keys(), gp_avg_rel_improvement.values(), label="VanillaGP", color="blue", marker="o")
    ax1.set_xlabel("Task Complexity")
    ax1.set_ylabel("Avg. Relative Improvement (%)")
    ax1.set_ylim(ymin=0)
    ax1.legend()
    ax1.set_title("Pixel Domain")

    # Robot
    domain = "robot"
    gp_avg_rel_improvement = gp_result_parser_robot.rel_improvement_by_complexity(domain)
    ax2.plot(gp_avg_rel_improvement.keys(), gp_avg_rel_improvement.values(), label="VanillaGP", color="blue", marker="o")
    ax2.set_xlabel("Task Complexity")
    ax2.set_ylabel("Avg. Relative Improvement (%)")
    ax2.set_ylim(ymin=0)
    ax2.legend()
    ax2.set_title("Robot Domain")

    # String
    domain = "string"
    gp_avg_rel_improvement = gp_result_parser_string.rel_improvement_by_complexity(domain)
    ax3.plot(gp_avg_rel_improvement.keys(), gp_avg_rel_improvement.values(), label="VanillaGP", color="blue", marker="o")
    ax3.set_xlabel("Task Complexity")
    ax3.set_ylabel("Avg. Relative Improvement (%)")
    ax3.set_ylim(ymin=0)
    ax3.legend()
    ax3.set_title("String Domain")

    plt.savefig("plots/relative_improvement.svg")
    fig.clf()
    plt.close

plot_rel_improvement()
plot_complexity_vs_solved_percentage()
# plot_error_progression("string", "strings/1-58-1.pl")
