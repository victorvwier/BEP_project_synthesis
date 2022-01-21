import matplotlib
from adjustText import adjust_text

from results_processing import ResultParser
import numpy as np
import matplotlib.pyplot as plt
import matplotx
import re


matplotlib.rc("axes", edgecolor="r")

algorithms = [
    "AS",
    "Brute",
    # "GA",
    "MH",
    "MUTE",
    "VLNS"
]

pixel_results_directory = "results/experiment1/pixel/"
# pixel_astar_results = ResultParser(pixel_results_directory + "Astar-20211216-165516.txt")
pixel_astar_results = ResultParser("results/redo-experiment 1/results/pixel/Astar-20220114-100158.txt")
# pixel_brute_results = ResultParser(pixel_results_directory + "brute-20211216-165130.txt")
pixel_brute_results = ResultParser("results/redo-experiment 1/results/pixel/brute-20220114-100130.txt")
# pixel_ga_results = ResultParser(pixel_results_directory + "gp-20211216-165347.txt")
pixel_ga_results = ResultParser("results/redo-experiment 1/results/pixel/gp-20220114-100156.txt")
pixel_mcts_results = ResultParser(pixel_results_directory + "mcts-20211216-165228.txt")
pixel_metro_results = ResultParser(pixel_results_directory + "metro-20211216-165034.txt")
pixel_vlns_results = ResultParser(pixel_results_directory + "VLNS-20211216-165352.txt")
pixel_results_per_algorithm = dict({
    "AS": pixel_astar_results,
    "Brute": pixel_brute_results,
    "GA": pixel_ga_results,
    "MUTE": pixel_mcts_results,
    "MH": pixel_metro_results,
    "VLNS": pixel_vlns_results,
})

robot_results_directory = "results/experiment1/robot/"
# robot_astar_results = ResultParser(robot_results_directory + "Astar-20211216-042641.txt")
robot_astar_results = ResultParser("results/redo-experiment 1/results/robot/Astar-20220114-100115.txt")
# robot_brute_results = ResultParser(robot_results_directory + "brute-20211216-042609.txt")
robot_brute_results = ResultParser("results/redo-experiment 1/results/robot/brute-20220114-100113.txt")
# robot_ga_results = ResultParser(robot_results_directory + "gp-20211216-042625.txt")
robot_ga_results = ResultParser("results/redo-experiment 1/results/robot/gp-20220114-100114.txt")
robot_mcts_results = ResultParser(robot_results_directory + "mcts-20211216-042616.txt")
robot_metro_results = ResultParser(robot_results_directory + "metro-20211216-042605.txt")
robot_vlns_results = ResultParser(robot_results_directory + "VLNS-20211216-042630.txt")
robot_results_per_algorithm = dict({
    "AS": robot_astar_results,
    "Brute": robot_brute_results,
    "GA": robot_ga_results,
    "MUTE": robot_mcts_results,
    "MH": robot_metro_results,
    "VLNS": robot_vlns_results,
})

string_results_directory = "results/experiment1/string/"
# string_astar_results = ResultParser(string_results_directory + "Astar-20211217-003335.txt")
string_astar_results = ResultParser("results/redo-experiment 1/results/string/Astar-20220114-102121.txt")
# string_brute_results = ResultParser(string_results_directory + "brute-20211216-174005.txt")
string_brute_results = ResultParser("results/redo-experiment 1/results/string/brute-20220114-100143.txt")
# string_ga_results = ResultParser(string_results_directory + "gp-20211216-180241.txt")
string_ga_results = ResultParser("results/redo-experiment 1/results/string/gp-20220114-101241.txt")
string_mcts_results = ResultParser(string_results_directory + "mcts-20211216-175106.txt")
string_metro_results = ResultParser(string_results_directory + "metro-20211216-172813.txt")
string_vlns_results = ResultParser(string_results_directory + "VLNS-20211216-181329.txt")
string_results_per_algorithm = dict({
    "AS": string_astar_results,
    "Brute": string_brute_results,
    "GA": string_ga_results,
    "MUTE": string_mcts_results,
    "MH": string_metro_results,
    "VLNS": string_vlns_results,
})


def get_solved_results(result_parser):
    all_results = result_parser.get_result()

    def solved(result):
        return result["test_cost"] + result["train_cost"] == 0

    return list(filter(solved, all_results))


def filter_solved_results(results):
    def solved(result):
        return result["test_cost"] + result["train_cost"] == 0

    return list(filter(solved, results))


def filter_results_with_complexity(complexity, results):
    def has_wanted_complexity(result):
        filename = result["file"]
        return bool(re.match(r".+/%s-.+?-.+pl" % complexity, filename))

    return list(filter(has_wanted_complexity, results))


def filter_selected_robot_or_pixel_tasks(results):
    def has_wanted_complexity(result):
        filename = result["file"]
        return bool(re.match(r".+/.+-[0-4]-.+pl", filename))

    return list(filter(has_wanted_complexity, results))


foreground = "#f8f8f2"
background = "#434343ff"
comment = "white"
# comment = "#6272a4"
dark_theme = {
    # "grid.color": "pink",
    "lines.color": foreground,
    "patch.edgecolor": foreground,
    "text.color": foreground,
    "axes.facecolor": background,
    "axes.edgecolor": foreground,
    "axes.labelcolor": foreground,
    "xtick.color": foreground,
    "ytick.color": foreground,
    "legend.framealpha": 0,
    "grid.color": comment,
    "figure.facecolor": background,
    "figure.edgecolor": background,
    "savefig.facecolor": background,
    "savefig.edgecolor": background,
    "boxplot.boxprops.color": foreground,
    "boxplot.capprops.color": foreground,
    "boxplot.flierprops.color": foreground,
    "boxplot.flierprops.markeredgecolor": foreground,
    "boxplot.whiskerprops.color": foreground,
    # "axes.prop_cycle": mpl.cycler(color=cycle),
}


def plot_success_per_complexity_string():
    with plt.style.context(matplotx.styles.duftify({
        "grid.color": "black",
    })):
    # with plt.style.context(matplotx.styles.duftify(dark_theme)):
        for algorithm in algorithms:
            all_results = string_results_per_algorithm[algorithm].get_result()
            percentages = []
            for complexity in range(1, 10):
                results_per_complexity = filter_results_with_complexity(complexity, all_results)
                total_successes = len(filter_solved_results(results_per_complexity))
                percentage = 100.0 * total_successes / len(results_per_complexity)
                percentages.append(percentage)
            plt.plot(range(1, 10), percentages, label=algorithm, marker='o')

        matplotx.line_labels(min_label_distance=5)
        plt.ylim(0, 103)
        plt.xticks(range(1, 10))
        plt.xlim(1, 9)
        plt.xlabel("No. training examples"
                   # , fontsize=13
                   )
        plt.ylabel("Tasks solved (%)"
                   # , fontsize=13
                   )
        # plt.legend(prop={'size': 13})

        # plt.savefig("dark_string_percentage.svg", bbox_inches='tight')
        # plt.savefig("dark_string_percentage.png", bbox_inches='tight')
        plt.savefig("light_string_percentage.svg", bbox_inches='tight')
        plt.savefig("light_string_percentage.png", bbox_inches='tight')
        plt.show()


def plot_success_per_complexity_robot():
    with plt.style.context(matplotx.styles.duftify({
        "grid.color": "black",
    })):
    # with plt.style.context(matplotx.styles.duftify(dark_theme)):
        for algorithm in algorithms:
            all_results = robot_results_per_algorithm[algorithm].get_result()

            # only use tasks that were selected for testing, so none of the data that was used for training is used.
            filtered_results = filter_selected_robot_or_pixel_tasks(all_results)
            percentages = []

            for complexity in range(2, 11, 2):
                results_per_complexity = filter_results_with_complexity(complexity, filtered_results)
                total_successes = len(filter_solved_results(results_per_complexity))
                percentage = 100.0 * total_successes / len(results_per_complexity)
                percentages.append(percentage)
            ax = plt.plot(range(2, 11, 2), percentages, label=algorithm, marker='o')

        matplotx.line_labels(min_label_distance=5)
        # matplotx.ylabel_top("Tasks solved (%)")
        # ax.xaxis.label.set_color("red")
        plt.ylim(0, 103)
        plt.xticks(range(2, 11, 2))
        plt.xlim(2, 10)
        plt.xlabel(
            "Grid size",
            # fontsize=13
        )
        plt.ylabel(
            "Tasks solved (%)",
            # fontsize=13
        )
        # plt.legend(prop={'size': 13})
        # plt.savefig("dark_robot_percentage.svg", bbox_inches='tight')
        # plt.savefig("dark_robot_percentage.png", bbox_inches='tight')
        plt.savefig("light_robot_percentage.svg", bbox_inches='tight')
        plt.savefig("light_robot_percentage.png", bbox_inches='tight')
        plt.show()


def plot_success_per_complexity_pixel():
    with plt.style.context(matplotx.styles.duftify({
        "grid.color": "black",
    })):
    # with plt.style.context(matplotx.styles.duftify(dark_theme)):
        for algorithm in algorithms:
            all_results = pixel_results_per_algorithm[algorithm].get_result()

            # only use tasks that were selected for testing, so none of the data that was used for training is used.
            filtered_results = filter_selected_robot_or_pixel_tasks(all_results)
            percentages = []

            for complexity in range(1, 6):
                results_per_complexity = filter_results_with_complexity(complexity, filtered_results)
                total_successes = len(filter_solved_results(results_per_complexity))
                percentage = 100.0 * total_successes / len(results_per_complexity)
                percentages.append(percentage)
            plt.plot(range(1, 6), percentages, label=algorithm, marker='o')

        matplotx.line_labels(min_label_distance=5)
        plt.ylim(0, 103)
        plt.xticks(range(1, 6))
        plt.xlim(1, 5)
        plt.xlabel(
            "No. symbols",
            # fontsize=13
        )
        plt.ylabel(
            "Tasks solved (%)",
            # fontsize=13
        )
        # plt.legend(prop={'size': 13})
        print(plt.axes)
        # plt.savefig("dark_pixel_percentage.svg", bbox_inches='tight')
        # plt.savefig("dark_pixel_percentage.png", bbox_inches='tight')
        plt.savefig("light_pixel_percentage.svg", bbox_inches='tight')
        plt.savefig("light_pixel_percentage.png", bbox_inches='tight')
        plt.show()

graph_colors = dict({
    "AS": "tab:blue",
    "Brute": "tab:orange",
    # "GA": "tab:green",
    "MUTE": "tab:green",
    "MH": "tab:red",
    "VLNS": "tab:purple",
})

def plot_time_vs_success_string():
    with plt.style.context(matplotx.styles.duftify({
        "grid.color": "black",
    })):
    # with plt.style.context(matplotx.styles.duftify(dark_theme)):
        fig, ax = plt.subplots()
        texts = []

        for algorithm in algorithms:
            all_results = string_results_per_algorithm[algorithm].get_result()
            percentages = []
            average_execution_times = []
            all_execution_times = []

            for complexity in range(1, 10):
                results_per_complexity = filter_results_with_complexity(complexity, all_results)
                solved_results = filter_solved_results(results_per_complexity)
                total_successes = len(solved_results)
                percentage = 100.0 * total_successes / len(results_per_complexity)
                percentages.append(percentage)
                execution_times = list(map(lambda res: res["execution_time"], solved_results))
                if len(execution_times) > 0:
                    average_execution_time = sum(execution_times) / len(execution_times)
                    all_execution_times.extend(execution_times)
                    percentages.append(percentage)
                else:
                    average_execution_time = 0
                average_execution_times.append(average_execution_time)

                # ax.scatter(average_execution_times, percentages, label=algorithm, alpha=0.4)
                # ax.scatter(np.mean(average_execution_times), np.mean(percentages), color=graph_colors[algorithm], label=algorithm)
            ax.scatter(np.mean(all_execution_times), np.mean(percentages), color=graph_colors[algorithm],
                       label=algorithm)
            texts.append(
                plt.text(np.mean(all_execution_times), np.mean(percentages), algorithm, color=graph_colors[algorithm])
            )
        adjust_text(texts)

        plt.ylim(0, 103)
        plt.xlim(0, 2)
        plt.xlabel("Average execution time of solved tasks (sec)")
        plt.ylabel(
            "Tasks solved (%)",
            # fontsize=13,
        )
        # plt.legend()
        # plt.legend(prop={'size': 13})
        # plt.savefig("dark_string_time.svg", bbox_inches='tight')
        # plt.savefig("dark_string_time.png", bbox_inches='tight')
        plt.savefig("light_string_time.svg", bbox_inches='tight')
        plt.savefig("light_string_time.png", bbox_inches='tight')
        plt.show()


def plot_time_vs_success_robot():
    with plt.style.context(matplotx.styles.duftify({
        "grid.color": "black",
    })):
    # with plt.style.context(matplotx.styles.duftify(dark_theme)):
        fig, ax = plt.subplots()
        texts = []

        for algorithm in algorithms:
            all_results = robot_results_per_algorithm[
                algorithm].get_result()  # only use tasks that were selected for testing, so none of the data that was used for training is used.
            filtered_results = filter_selected_robot_or_pixel_tasks(all_results)

            percentages = []
            average_execution_times = []
            all_execution_times = []

            for complexity in range(2, 11, 2):
                results_per_complexity = filter_results_with_complexity(complexity, filtered_results)
                solved_results = filter_solved_results(results_per_complexity)
                total_successes = len(solved_results)
                percentage = 100.0 * total_successes / len(results_per_complexity)
                percentages.append(percentage)
                execution_times = list(map(lambda res: res["execution_time"], solved_results))
                if len(execution_times) > 0:
                    average_execution_time = sum(execution_times) / len(execution_times)
                    all_execution_times.extend(execution_times)
                    percentages.append(percentage)
                else:
                    average_execution_time = 0
                average_execution_times.append(average_execution_time)

                # ax.scatter(average_execution_times, percentages, label=algorithm, alpha=0.4)
                # ax.scatter(np.mean(average_execution_times), np.mean(percentages), color=graph_colors[algorithm], label=algorithm)
            ax.scatter(np.mean(all_execution_times), np.mean(percentages), color=graph_colors[algorithm],
                       label=algorithm)
            texts.append(
                plt.text(np.mean(all_execution_times), np.mean(percentages), algorithm, color=graph_colors[algorithm])
            )
        adjust_text(texts,
                #     expand_text=(1.05, 1.2), expand_points=(1.05, 1.2),
                # expand_objects=(1.05, 1.2), expand_align=(1.5, 1.5)
        )
        plt.ylim(0, 103)
        plt.xlim(0, 0.8)
        plt.xlabel("Average execution time of solved tasks (sec)")
        plt.ylabel(
            "Tasks solved (%)",
            # fontsize=13
        )
        # plt.legend(prop={'size': 13})
        # plt.legend()
        # plt.savefig("dark_robot_time.svg", bbox_inches='tight')
        # plt.savefig("dark_robot_time.png", bbox_inches='tight')
        plt.savefig("light_robot_time.svg", bbox_inches='tight')
        plt.savefig("light_robot_time.png", bbox_inches='tight')
        plt.show()


def plot_time_vs_success_pixel():
    with plt.style.context(matplotx.styles.duftify({
        "grid.color": "black",
    })):
    # with plt.style.context(matplotx.styles.duftify(dark_theme)):
        fig, ax = plt.subplots()
        texts = []
        other_points = []

        for algorithm in algorithms:
            all_results = pixel_results_per_algorithm[
                algorithm].get_result()  # only use tasks that were selected for testing, so none of the data that was used for training is used.
            filtered_results = filter_selected_robot_or_pixel_tasks(all_results)

            percentages = []
            average_execution_times = []
            all_execution_times = []

            for complexity in range(1, 6):
                results_per_complexity = filter_results_with_complexity(complexity, filtered_results)
                solved_results = filter_solved_results(results_per_complexity)
                total_successes = len(solved_results)
                percentage = 100.0 * total_successes / len(results_per_complexity)
                percentages.append(percentage)
                execution_times = list(map(lambda res: res["execution_time"], solved_results))
                if len(execution_times) > 0:
                    average_execution_time = sum(execution_times) / len(execution_times)
                    all_execution_times.extend(execution_times)
                    percentages.append(percentage)
                else:
                    average_execution_time = 0
                average_execution_times.append(average_execution_time)

            # ax.scatter(average_execution_times, percentages, label=algorithm, alpha=0.4)
            # ax.scatter(np.mean(average_execution_times), np.mean(percentages), color=graph_colors[algorithm], label=algorithm)
            ax.scatter(np.mean(all_execution_times), np.mean(percentages), color=graph_colors[algorithm], label=algorithm)
            texts.append(
                plt.text(np.mean(all_execution_times), np.mean(percentages), algorithm, color=graph_colors[algorithm])
            )
            other_points.append((np.mean(all_execution_times), np.mean(percentages)))

        adjust_text(
            texts,
            # expand_text=(2, 2),
            # expand_points=(2, 2),
            # expand_objects=(2, 2),
            # add_objects=other_points
        )


        plt.ylim(0, 103)
        plt.xlim(0, 6)
        plt.xlabel("Average execution time of solved tasks (sec)")
        plt.ylabel("Tasks solved (%)")
        # plt.legend(prop={'size': 13})
        # plt.savefig("dark_pixel_time.svg", bbox_inches='tight')
        # plt.savefig("dark_pixel_time.png", bbox_inches='tight')
        plt.savefig("light_pixel_time.svg", bbox_inches='tight')
        plt.savefig("light_pixel_time.png", bbox_inches='tight')
        plt.show()


def find_differences_in_solved_string_tasks_brute_and_mute():
    solved_by_both = []
    solved_by_mute_only = []
    solved_by_brute_only = []
    solved_by_neither = []

    for (result_brute, result_mute) in zip(
            string_brute_results_experiment_2.filter_result_fields(["file", "test_cost"]),
            string_mcts_results_experiment_2.filter_result_fields(["file", "test_cost"])):
        assert (result_brute[0] == result_mute[0])
        file_name = result_brute[0]
        if not (bool(re.match(r".+/[159]-.+?-1.+pl", file_name))):
            continue

        costs_brute = result_brute[1]
        costs_mute = result_mute[1]
        print("Pair: %s" % str((result_brute, result_mute)))
        # see if both solved the task
        if costs_brute == 0 and costs_mute == 0:
            solved_by_both.append(file_name)
        elif costs_brute == 0 and costs_mute > 0:
            solved_by_brute_only.append(file_name)
        elif costs_mute == 0 and costs_brute > 0:
            solved_by_mute_only.append(file_name)
        elif costs_mute > 0 and costs_brute > 0:
            solved_by_neither.append(file_name)
        else:
            raise Exception("something went wrong. one of the earlier statements should have been true")

    print("solved by both: (length: %s) %s" % (len(solved_by_both), str(solved_by_both)))
    print("solved by mute only: (length: %s) %s" % (len(solved_by_mute_only), str(solved_by_mute_only)))
    print("solved by brute only: (length: %s) %s" % (len(solved_by_brute_only), str(solved_by_brute_only)))
    print("solved by neither: (length: %s) %s" % (len(solved_by_neither), str(solved_by_neither)))


if __name__ == "__main__":
    # find_differences_in_solved_string_tasks_brute_and_mute()

    plot_success_per_complexity_string()
    plot_success_per_complexity_robot()
    plot_success_per_complexity_pixel()
    #
    plot_time_vs_success_string()
    plot_time_vs_success_robot()
    plot_time_vs_success_pixel()

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
