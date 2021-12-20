from results_processing import ResultParser
# import numpy as np
# import matplotlib as mpl
import matplotlib.pyplot as plt
import re

algorithms = ["astar", "brute", "ga", "mcts", "metro", "vlns"]

pixel_results_directory = "results/experiment1/pixel/"
pixel_astar_results = ResultParser(pixel_results_directory + "Astar-20211216-165516.txt")
pixel_brute_results = ResultParser(pixel_results_directory + "brute-20211216-165130.txt")
pixel_ga_results = ResultParser(pixel_results_directory + "gp-20211216-165347.txt")
pixel_mcts_results = ResultParser(pixel_results_directory + "mcts-20211216-165228.txt")
pixel_metro_results = ResultParser(pixel_results_directory + "metro-20211216-165034.txt")
pixel_vlns_results = ResultParser(pixel_results_directory + "VLNS-20211216-165352.txt")
pixel_results_per_algorithm = dict({
    "astar": pixel_astar_results,
    "brute": pixel_brute_results,
    "ga": pixel_ga_results,
    "mcts": pixel_mcts_results,
    "metro": pixel_metro_results,
    "vlns": pixel_vlns_results,
})

robot_results_directory = "results/experiment1/robot/"
robot_astar_results = ResultParser(robot_results_directory + "Astar-20211216-042641.txt")
robot_brute_results = ResultParser(robot_results_directory + "brute-20211216-042609.txt")
robot_ga_results = ResultParser(robot_results_directory + "gp-20211216-042625.txt")
robot_mcts_results = ResultParser(robot_results_directory + "mcts-20211216-042616.txt")
robot_metro_results = ResultParser(robot_results_directory + "metro-20211216-042605.txt")
robot_vlns_results = ResultParser(robot_results_directory + "VLNS-20211216-042630.txt")
robot_results_per_algorithm = dict({
    "astar": robot_astar_results,
    "brute": robot_brute_results,
    "ga": robot_ga_results,
    "mcts": robot_mcts_results,
    "metro": robot_metro_results,
    "vlns": robot_vlns_results,
})

string_results_directory = "results/experiment1/string/"
string_astar_results = ResultParser(string_results_directory + "Astar-20211217-003335.txt")
string_brute_results = ResultParser(string_results_directory + "brute-20211216-174005.txt")
string_ga_results = ResultParser(string_results_directory + "gp-20211216-180241.txt")
string_mcts_results = ResultParser(string_results_directory + "mcts-20211216-175106.txt")
string_metro_results = ResultParser(string_results_directory + "metro-20211216-172813.txt")
string_vlns_results = ResultParser(string_results_directory + "VLNS-20211216-181329.txt")
string_results_per_algorithm = dict({
    "astar": string_astar_results,
    "brute": string_brute_results,
    "ga": string_ga_results,
    "mcts": string_mcts_results,
    "metro": string_metro_results,
    "vlns": string_vlns_results,
})


def get_solved_results(result_parser):
    solved_results = []
    all_results = result_parser.get_result()

    def solved(result):
        return result["test_cost"] + result["train_cost"] == 0

    return list(filter(solved, all_results))
    # for result in all_results:
    #     if result["test_cost"] + result["train_cost"] == 0:
    #         solved_results.append(result)
    # return solved_results


def filter_solved_results(results):
    def solved(result):
        return result["test_cost"] + result["train_cost"] == 0

    return list(filter(solved, results))


# solved_pixel_astar_results = get_solved_results(pixel_astar_results)
# solved_pixel_brute_results = get_solved_results(pixel_brute_results)
# solved_pixel_ga_results = get_solved_results(pixel_ga_results)
# solved_pixel_mcts_results = get_solved_results(pixel_mcts_results)
# solved_pixel_metro_results = get_solved_results(pixel_metro_results)
# solved_pixel_vlns_results = get_solved_results(pixel_vlns_results)
#
# solved_robot_astar_results = get_solved_results(robot_astar_results)
# solved_robot_brute_results = get_solved_results(robot_brute_results)
# solved_robot_ga_results = get_solved_results(robot_ga_results)
# solved_robot_mcts_results = get_solved_results(robot_mcts_results)
# solved_robot_metro_results = get_solved_results(robot_metro_results)
# solved_robot_vlns_results = get_solved_results(robot_vlns_results)
#
# solved_string_astar_results = get_solved_results(string_astar_results)
# solved_string_brute_results = get_solved_results(string_brute_results)
# solved_string_ga_results = get_solved_results(string_ga_results)
# solved_string_mcts_results = get_solved_results(string_mcts_results)
# solved_string_metro_results = get_solved_results(string_metro_results)
# solved_string_vlns_results = get_solved_results(string_vlns_results)

def filter_results_with_complexity(complexity, results):
    def has_wanted_complexity(result):
        filename = result["file"]
        return bool(re.match(r".+/%s-.+?-.+pl" % complexity, filename))

    return list(filter(has_wanted_complexity, results))


def plot_success_per_complexity_string():
    for algorithm in algorithms:
        all_results = string_results_per_algorithm[algorithm].get_result()
        percentages = []
        for complexity in range(1, 10):
            results_per_complexity = filter_results_with_complexity(complexity, all_results)
            total_successes = len(filter_solved_results(results_per_complexity))
            percentage = 100.0 * total_successes / len(results_per_complexity)
            percentages.append(percentage)
        plt.plot(range(1, 10), percentages, label=algorithm)

    plt.ylim(0, 100)
    plt.legend()
    plt.show()

    pass


if __name__ == "__main__":

    plot_success_per_complexity_string()

    # # results_name = "results/experiment1/robot/mcts-20211215-165729.txt"
    # # results = ResultParser(results_name)
    # results = robot_mcts_results
    # # results2 = ResultParser("results/robot/metro-20211213-143001.json")
    # # results3 = ResultParser("results/robot/VLNS-20211213-143323.json")
    #
    # data = list(zip(*results.filter_result_fields(['program_length', 'execution_time'])))
    # # data2 = list(zip(*results2.filter_result_fields(['program_length', 'execution_time'])))
    # # data3 = list(zip(*results3.filter_result_fields(['program_length', 'execution_time'])))
    # X = data[0]
    # Y = data[1]
    #
    # # X2 = data2[0]
    # # Y2 = data2[1]
    #
    # # X3 = data3[0]
    # # Y3 = data3[1]
    #
    # fig, ax = plt.subplots()
    # ax.scatter(X, Y)
    # # ax.scatter(X2, Y2)
    # # ax.scatter(X3, Y3)
    # fig.show()
