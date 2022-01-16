import json
from matplotlib import pyplot as plt
from pathlib import Path
import glob

from example_parser.string_parser import StringParser

plt.rcParams["figure.dpi"] = plt.rcParamsDefault["figure.dpi"]
plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]


def post_process(nd: dict):
    for name, data in nd.items():
        accuracies = []
        solutions_found = 0
        for i, case in enumerate(data):
            n_examples = case['test_amount']
            n_correct = case['test_amount_correct']
            accuracy = float(n_correct) / n_examples * 100
            accuracies.append(accuracy)
            path = Path(case['file'])
            n1, n2, n3 = path.stem.split("-")
            solution_found = case.get('solution_found', (True if case['train_cost'] == 0 else False))
            fully_correct = solution_found and case['test_amount_correct'] == case['test_amount']
            nd[name][i].update({
                'n_examples': n_examples,
                'n_correct': n_correct,
                'accuracy': accuracy,
                'solution_found': solution_found,
                'fully_correct': fully_correct,
                'n1': n1,
                'n2': n2,
                'n3': n3,
            })
    return nd


def load_from_directory(path: str, include_cost_traces=False):
    name_fname = {}
    for fname in glob.glob(str(Path(path).joinpath("*.txt"))):
        name = fname.split("/")[-1].rsplit(".", 1)[0]
        name_fname[name] = fname
    nd = {}
    for name, fname in name_fname.items():
        with open(fname, mode="r") as file:
            data = []
            for line in file.readlines():
                line_data = json.loads(line)
                if not include_cost_traces:
                    line_data.pop('cost_per_iteration', None)
                    line_data.pop('g_cost_per_iteration', None)
                data.append(line_data)
            nd[name] = data
    return post_process(nd)

def aggregate(nd: dict):
    name_aggregate = {}
    for name, data in nd.items():
        accuracies = [c['test_amount_correct']/c['test_amount']*100 for c in data]
        n_cases = len(data)
        n_solved = sum([int(c['solution_found']) for c in data])
        exec_time = sum([c['execution_time'] for c in data if c['solution_found']]) / n_solved
        program_length = sum([float(c['program_length']) for c in data if c['solution_found']]) / n_solved
        accuracy = sum(accuracies) / len(accuracies)
        solutions_found = sum(c['solution_found'] for c in data)
        correctness = float(solutions_found) / n_cases * 100
        fully_correctness = sum(c['solution_found'] and c['test_amount_correct'] == c['test_amount'] for c in data) / n_cases * 100
        aggregate_data = {
            'n_cases': n_cases,
            'n_solved': n_solved,
            'exec_time': exec_time,
            'program_length': program_length,
            'accuracy': accuracy,
            'correctness': correctness,
            'fully_correctness': fully_correctness,
        }
        name_aggregate[name] = aggregate_data
    return name_aggregate


def avg_prop_by_prop(data: list[dict], key, by_key, only_solved=False):
    result = {}
    for case in data:
        if only_solved and case['solution_found'] == False:
            continue
        by_prop = case[by_key]
        result[by_prop] = result.get(by_prop, []) + [case[key]]
    for by_prop in result:
        result[by_prop] = float(sum(result[by_prop])) / len(result[by_prop])
    return result


def keep_commonly_solved(nd: dict[str, list]):
    nd_all_solved = {}
    for name in name_data_subset:
        nd_all_solved[name] = []
    for i, _ in enumerate(list(nd.values())[0]):
        all_solved = all([data[i]['solution_found'] for name, data in nd.items()])
        if all_solved:
            for name in nd_all_solved:
                nd_all_solved[name].append(nd[name][i])
    return nd_all_solved


def keep_names(nd: dict, names: list):
    return {k: v for k, v in nd.items() if k in names}


def print_string_case(case_id):
    fname = f"{case_id}.pl"
    test_case = StringParser().parse_file(fname)
    for ex in test_case.training_examples:
        print()
        print(ex.input_environment.to_string())
        print(ex.output_environment.to_string())

#%%


name_data = load_from_directory("../final_results2/string")
name_aggregate = aggregate(name_data)
print(json.dumps(name_aggregate, indent=2))

#%%

name_data = load_from_directory("../final_results2/string")
brute = name_data['brute']
astar = name_data['astar']

impossible_cases = set(c['file'].split("/")[-1].split(".")[0] for c in astar if c['train_cost'] == float('inf'))

for case_id in impossible_cases:
    print(case_id)
    # print_string_case(case_id)
    # print("-----------------")

all_cases = set(c['file'].split("/")[-1].split(".")[0] for c in brute + astar)
solved_brute = set(c['file'].split("/")[-1].split(".")[0] for c in brute if c['solution_found'])
solved_astar = set(c['file'].split("/")[-1].split(".")[0] for c in astar if c['solution_found'])
unsolved_cases = all_cases.difference(solved_brute, solved_astar)
remaining_cases = unsolved_cases.difference(impossible_cases)

print(f"Impossible cases: {len(impossible_cases)}")
print(f"Total cases: {len(all_cases)}")
print(f"Solved by Brute: {len(solved_brute)}")
print(f"Solved by Astar: {len(solved_astar)}")
print()
print(f"Solved by Brute, but not Astar: {len(solved_brute.difference(solved_astar))}")
print(f"Solved by Astar, but not Brute: {len(solved_astar.difference(solved_brute))}")
print(f"Solved by neither: {len(unsolved_cases)}")
print(f"Solved by neither, but possible: {len(remaining_cases)}")

# print(f'[{", ".join(['"%s"' for c in solved_brute.difference(solved_astar)])}]')
case_id_strings = [f"'{c}'" for c in solved_astar.difference(solved_brute)]
print(f'[{",".join(case_id_strings)}]')


# for case_id in remaining_cases:
#     print_string_case(case_id)
#     print("-----------------")



#%%


name_data = load_from_directory("../final_results2/string")
name_data_subset = keep_names(name_data, ["brute_old_ls", "brute_ls", "astar_ls", "brute", "astar"])
name_data_all_solved = keep_commonly_solved(name_data_subset)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1)
fig.set_size_inches(6.4, 18)

for name, data in name_data_subset.items():
    plot_data = avg_prop_by_prop(data, 'accuracy', 'n1', only_solved=False)
    ax1.plot(plot_data.keys(), plot_data.values(), "o-", label=name)
    ax1.set_xlabel("no. examples")
    ax1.set_ylabel("predictive accuracy [%]")
    ax1.set_ylim((0, 100))
for name, data in name_data_all_solved.items():
    plot_data = avg_prop_by_prop(data, 'execution_time', 'n1', only_solved=True)
    ax2.plot(plot_data.keys(), plot_data.values(), "o-", label=name)
    ax2.set_xlabel("no. examples")
    ax2.set_ylabel("mean learning time [s]")
    # ax2.set_ylim((0, 5))
for name, data in name_data_all_solved.items():
    plot_data = avg_prop_by_prop(data, 'program_length', 'n1', only_solved=True)
    ax3.plot(plot_data.keys(), plot_data.values(), "o-", label=name)
    ax3.set_xlabel("no. examples")
    ax3.set_ylabel("mean program length")
for name, data in name_data_subset.items():
    plot_data = avg_prop_by_prop(data, 'solution_found', 'n1', only_solved=False)
    plot_data = {k: v*100 for k, v in plot_data.items()}
    ax4.plot(plot_data.keys(), plot_data.values(), "o-", label=name)
    ax4.set_xlabel("no. examples")
    ax4.set_ylabel("solve rate [%]")
    ax4.set_ylim((0, 100))

plt.title("Basic improvements")
plt.legend()
plt.tight_layout()
plt.show()

#%%

name_data_subset = keep_names(name_data, ["brute", "astar"])
name_data_all_solved = keep_commonly_solved(name_data_subset)

fig, axs = plt.subplots(len(name_data_all_solved), 1, sharex=True)
fig.set_size_inches(6.4, 10)
for i, (name, data) in enumerate(name_data_all_solved.items()):
    x = [c['program_length'] for c in data]
    axs[i].hist(x, bins=range(0, 150, 10))
    axs[i].set_title(name)
    axs[i].set_xlim((0, 150))
    axs[i].set_ylim((1, 10**4))
    # axs[i].set_ylim((0, 6000))
    axs[i].set_yscale('log')

plt.show()


#%%

for name, data in name_data.items():
    size_accuracy = avg_prop_by_prop(data, 'execution_time', 'n1', only_solved=False)
    plt.plot(size_accuracy.keys(), size_accuracy.values(), "o-", label=name)

plt.legend()
plt.show()

#%%


for name, data in name_data.items():
    size_accuracy = avg_prop_by_prop(data, 'program_length', 'n1', only_solved=True)
    plt.plot(size_accuracy.keys(), size_accuracy.values(), "o-", label=name)

plt.legend()
plt.show()


#%%

def plot_aggregate(xprop, yprop, name_aggregate_data):
    for name, data in name_aggregate_data.items():
        plt.scatter(data[xprop], data[yprop], label=name)
        plt.annotate(name, (data[xprop], data[yprop]))
    plt.xlabel(xprop)
    plt.ylabel(yprop)
    # plt.xlim(left=0)
    # plt.ylim(bottom=0)


plot_aggregate("correctness", "accuracy", keep_names(name_aggregate, ["astar_ls", "brute_ls", "astar", "brute"]))
plt.show()


#%%
name_data = load_from_directory("../final_results2/string")
name_aggregate = aggregate(name_data)

plot_data_ls = {
    0: name_aggregate["brute_ls"],
    0.25: name_aggregate["astar0.25_ls"],
    0.5: name_aggregate["astar_ls"],
    0.75: name_aggregate["astar0.75_ls"],
    0.875: name_aggregate["astar0.875_ls"],
    1: name_aggregate["dijkstra_ls"]
}

plot_data = {
    0: name_aggregate["brute"],
    0.25: name_aggregate["astar0.25"],
    0.5: name_aggregate["astar"],
    0.75: name_aggregate["astar0.75"],
    0.875: name_aggregate["astar0.875"],
    1: name_aggregate["dijkstra"]
}

plt.plot(plot_data_ls.keys(), [v['accuracy'] for v in plot_data_ls.values()], "o-", label="levenshtein")
plt.plot(plot_data.keys(), [v['accuracy'] for v in plot_data.values()], "o-", label="alignment")
plt.xlabel("Weight")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

#%%
name_data = load_from_directory("../final_results2/pixel")
name_aggregate = aggregate(name_data)

plot_data_hamming = {
    0: name_aggregate["brute_hamming"],
    0.25: name_aggregate["astar0.25_hamming"],
    0.5: name_aggregate["astar_hamming"],
    0.75: name_aggregate["astar0.75_hamming"],
    0.875: name_aggregate["astar0.875_hamming"],
    1: name_aggregate["dijkstra_hamming"]
}

plot_data_furthest = {
    0: name_aggregate["brute_furthest"],
    0.25: name_aggregate["astar0.25_furthest"],
    0.5: name_aggregate["astar_furthest"],
    0.75: name_aggregate["astar0.75_furthest"],
    0.875: name_aggregate["astar0.875_furthest"],
    1: name_aggregate["dijkstra_furthest"]
}

plot_data = {
    0: name_aggregate["brute"],
    0.25: name_aggregate["astar0.25"],
    0.5: name_aggregate["astar"],
    0.75: name_aggregate["astar0.75"],
    0.875: name_aggregate["astar0.875"],
    1: name_aggregate["dijkstra"]
}

plt.plot(plot_data_hamming.keys(), [v['accuracy'] for v in plot_data_hamming.values()], "o-", label="hamming")
plt.plot(plot_data_furthest.keys(), [v['accuracy'] for v in plot_data_furthest.values()], "o-", label="furthest")
plt.plot(plot_data.keys(), [v['accuracy'] for v in plot_data.values()], "o-", label="triangle")
plt.xlabel("Weight")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

#%%
name_data = load_from_directory("../final_results2/robot")
name_aggregate = aggregate(name_data)

plot_data_manhattan = {
    0: name_aggregate["brute_manhattan"],
    0.25: name_aggregate["astar0.25_manhattan"],
    0.5: name_aggregate["astar_manhattan"],
    0.75: name_aggregate["astar0.75_manhattan"],
    0.875: name_aggregate["astar0.875_manhattan"],
    1: name_aggregate["dijkstra_manhattan"]
}

plot_data = {
    0: name_aggregate["brute"],
    0.25: name_aggregate["astar0.25"],
    0.5: name_aggregate["astar"],
    0.75: name_aggregate["astar0.75"],
    0.875: name_aggregate["astar0.875"],
    1: name_aggregate["dijkstra"]
}

plt.plot(plot_data_manhattan.keys(), [v['accuracy'] for v in plot_data_manhattan.values()], "o-", label="manhattan")
plt.plot(plot_data.keys(), [v['accuracy'] for v in plot_data.values()], "o-", label="stage-select")
plt.xlabel("Weight")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

#%%
name_data_subset = keep_names(name_data, ["brute_ls", "astar_ls", "brute", "astar"])
# name_data_subset = keep_names(name_data, ["brute_ls", "astar_ls", "brute", "astar"])
# name_data_all_solved = keep_commonly_solved(name_data_subset)

for name, data in name_data_subset.items():
    plot_data = avg_prop_by_prop(data, 'accuracy', 'n1', only_solved=False)
    plt.plot(plot_data.keys(), plot_data.values(), "o-", label=name)
    plt.ylim(bottom=0)
    plt.xlabel("no. examples")
    plt.ylabel("predictive accuracy [%]")
    plt.ylim((0, 100))

plt.title("Heuristic")
plt.legend()
plt.tight_layout()
plt.show()

#%%
b_case = next(c for c in name_data['brute_ls'] if c["file"] == "strings/1-17-2.pl")
a_case = next(c for c in name_data['astar_ls'] if c["file"] == "strings/1-17-2.pl")
b_costs = [cost for [i, cost] in b_case["cost_per_iteration"]]
a_costs = [cost for [i, cost] in a_case["cost_per_iteration"]]
print(b_costs)
plt.plot(range(len(b_costs)), b_costs)
plt.plot(range(len(a_costs)), a_costs)
plt.show()
