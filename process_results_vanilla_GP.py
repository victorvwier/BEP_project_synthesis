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

    def get_percentage_solved(self):
        solved, cases = self.get_solved_count()
        return str((solved / cases ) * 100) + "%"

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

    def rel_improvement_by_complexity(self, domain):
        rel_improvement = []
        with open(self.file, "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                data = json.JSONDecoder().decode(stripped_line)

                file_name = data["file"][len(domain)+2:]
                complexity = file_name.split('-')[0]

                initial_error = data["initial_error"]
                final_cost = data["train_cost"]
                if (initial_error == 0):
                    rel_improvement_entry = 100.0
                    rel_improvement.append((complexity, rel_improvement_entry))
                else:
                    rel_improvement_entry = ((initial_error - final_cost) / initial_error) * 100.0
                    rel_improvement.append((complexity, rel_improvement_entry))

        rel_imp_by_complexity = OrderedDict()
        for k, *v in rel_improvement:
            rel_imp_by_complexity.setdefault(k, []).append(v)

        complexity_list = list(rel_imp_by_complexity.items())
        rel_imp_by_complexity = []
        for (c, l_s) in complexity_list:
            l = sum(l_s, [])
            rel_imp_by_complexity.append((c, sum(l)/len(l)))

        return rel_imp_by_complexity

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
gp_file_name_pixel = "" # sys.argv[1]
gp_file_name_robot = sys.argv[1]
gp_file_name_string = "" # sys.argv[3]
gp_path_to_file_pixel = "./results/pixel/" + gp_file_name_pixel
gp_path_to_file_robot = "./results/robot/" + gp_file_name_robot
gp_path_to_file_string = "./results/string/" + gp_file_name_string

gp_result_parser_pixel = ResultParser(gp_path_to_file_pixel)
gp_result_parser_robot = ResultParser(gp_path_to_file_robot)
gp_result_parser_string = ResultParser(gp_path_to_file_string)

# Brute
brute_file_name_pixel = "" # sys.argv[4]
brute_file_name_robot = sys.argv[2]
brute_file_name_string = "" # sys.argv[6]
brute_path_to_file_pixel = "./results/pixel/" + brute_file_name_pixel
brute_path_to_file_robot = "./results/robot/" + brute_file_name_robot
brute_path_to_file_string = "./results/string/" + brute_file_name_string

brute_result_parser_pixel = ResultParser(brute_path_to_file_pixel)
brute_result_parser_robot = ResultParser(brute_path_to_file_robot)
brute_result_parser_string = ResultParser(brute_path_to_file_string)

# Processing
# print("Pixel, VanillaGP solved: ", gp_result_parser_pixel.get_percentage_solved())
print("Robot, VanillaGP solved: ", gp_result_parser_robot.get_percentage_solved())
# print("String, VanillaGP solved: ", gp_result_parser_string.get_percentage_solved())

# print("Pixel, Brute solved: ", brute_result_parser_pixel.get_percentage_solved())
print("Robot, Brute solved: ", brute_result_parser_robot.get_percentage_solved())
# print("String, Brute solved: ", brute_result_parser_string.get_percentage_solved())

# if (gp_file_name_pixel[0:2] == "gp"):
#     rel_imp_pixel = gp_result_parser_pixel.relative_improvement()
#     for file, imp in rel_imp_pixel:
#         print("Pixel example ", file, " improved by ", imp, "%")
    
#     rel_imp_robot = gp_result_parser_robot.relative_improvement()
#     for file, imp in rel_imp_pixel:
#         print(" Robot example ", file, " improved by ", imp, "%")
    
#     rel_imp_string = gp_result_parser_string.relative_improvement()
#     for file, imp in rel_imp_pixel:
#         print("String example ", file, " improved by ", imp, "%")
# Visualization

def plot_complexity_vs_solved():
    # # Pixel
    # brute_solved_by_complexity = brute_result_parser_pixel.get_solved_count_by_complexity("pixel")
    # gp_solved_by_complexity = gp_result_parser_pixel.get_solved_count_by_complexity("pixel")
    # fig, ax = plt.subplots()
    # ax.plot(*zip(*brute_solved_by_complexity), label="Brute", color="red")
    # ax.plot(*zip(*gp_solved_by_complexity), label="VanillaGP", color="blue")
    # ax.set_xlabel("Task Complexity")
    # ax.set_ylabel("# Samples Solved")
    # ax.legend()
    # ax.set_title("Pixel Domain")

    # plt.savefig("Plots/complexity_vs_solved_pixel.svg")
    # fig.clf()
    # plt.close

    # Robot
    brute_solved_by_complexity = brute_result_parser_robot.get_solved_count_by_complexity("robot")
    gp_solved_by_complexity = gp_result_parser_robot.get_solved_count_by_complexity("robot")
    fig, ax = plt.subplots()
    ax.plot(*zip(*brute_solved_by_complexity), label="Brute", color="red")
    ax.plot(*zip(*gp_solved_by_complexity), label="VanillaGP", color="blue")
    ax.set_xlabel("Task Complexity")
    ax.set_ylabel("# Samples Solved")
    ax.legend()
    ax.set_title("Robot Domain")

    plt.savefig("plots/complexity_vs_solved_robot.svg")
    fig.clf()
    plt.close

    # # String
    # brute_solved_by_complexity = brute_result_parser_string.get_solved_count_by_complexity("string")
    # gp_solved_by_complexity = gp_result_parser_string.get_solved_count_by_complexity("string")
    # fig, ax = plt.subplots()
    # ax.plot(*zip(*brute_solved_by_complexity), label="Brute", color="red")
    # ax.plot(*zip(*gp_solved_by_complexity), label="VanillaGP", color="blue")
    # ax.set_xlabel("Task Complexity")
    # ax.set_ylabel("# Samples Solved")
    # ax.legend()
    # ax.set_title("String Domain")

    # plt.savefig("Plots/complexity_vs_solved_string.svg")
    # fig.clf()
    # plt.close

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

def plot_rel_improvement(domains=["", "", ""]):
    fig, ax = plt.subplots()
    fig.set_figwidth(8)
    fig.set_figheight(6)

    gp_rel_improvement = []
    if (domains[0] == "pixel"):
        gp_rel_improvement = gp_result_parser_pixel.relative_improvement(domains[0])
        ax.plot(*zip(*gp_rel_improvement), label="VanillaGP {}".format(domains[0]), marker="o", color="limegreen")
    if (domains[1] == "robot"):
        gp_rel_improvement = gp_result_parser_robot.rel_improvement_by_complexity(domains[1])
        ax.plot(*zip(*gp_rel_improvement), label="VanillaGP {}".format(domains[1]), marker="o", color="dodgerblue")
    if (domains[2] == "string"):
        gp_rel_improvement = gp_result_parser_string.relative_improvement(domains[2])
        ax.plot(*zip(*gp_rel_improvement), label="VanillaGP {}".format(domains[2]), marker="o", color="crimson")

    start, end = 0, 100
    ax.yaxis.set_ticks(range(start, end, 5))
    ax.set_xlabel("Complexity")
    ax.set_ylabel("Avg. Relative Improvement (%)")
    ax.set_ylim(ymin=0)
    ax.set_xticks([])
    ax.legend()
    ax.set_title("Average Relative Improvement Grouped by Complexity")

    plt.savefig("plots/rel_improvement.svg")
    fig.clf()
    plt.close

plot_complexity_vs_solved()
# plot_error_progression("string", "strings/1-58-1.pl")
plot_rel_improvement(["", "robot", ""])
