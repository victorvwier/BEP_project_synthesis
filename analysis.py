import json
from matplotlib import pyplot as plt
from pathlib import Path

plt.rcParams["figure.dpi"] = plt.rcParamsDefault["figure.dpi"]
plt.rcParams["figure.figsize"] = (3, 3)

#%%
name_fname = {
    "A*": "results/string/Astar-20220106-163811.txt",
    "Brute": "results/string/Astar-20220106-183552.txt",
}

# name_fname = {
#     "1": "/tmp/pycharm_project_46/results/string/astar0.5-levenshtein-nocache.txt",
#     "2": "/tmp/pycharm_project_46/results/string/astar0-levenshtein-nocache.txt",
#     "3": "/tmp/pycharm_project_46/results/string/astar0.5-levenshtein-nocache-tiebreak.txt",
# }

name_data = {}
for name, fname in name_fname.items():
    file = open(fname, mode="r")
    data = []
    for line in file.readlines():
        data.append(json.loads(line))
    name_data[name] = data
    file.close()

#%%

for name, data in name_data.items():
    print(max([c['execution_time'] for c in data]))

#%%
name_aggregate = {}
for name, data in name_data.items():
    accuracies = []
    solutions_found = 0
    for i, case in enumerate(data):
        n_examples = case['train_amount'] + case['test_amount']
        n_correct = case['train_amount_correct'] + case['test_amount_correct']
        accuracy = n_correct/n_examples
        accuracies.append(accuracy)
        path = Path(case['file'])
        n1, n2, n3 = path.stem.split("-")
        name_data[name][i]['n_examples'] = n_examples
        name_data[name][i]['n_correct'] = n_correct
        name_data[name][i]['accuracy'] = accuracy
        name_data[name][i]['n1'] = n1
        name_data[name][i]['n2'] = n2
        name_data[name][i]['n3'] = n3
        if case['solution_found']:
            solutions_found += 1

    n_cases = len(data)
    n_solved = sum([int(c['solution_found']) for c in data])
    exec_time = sum([c['execution_time'] for c in data if c['solution_found']])/n_solved
    program_length = sum([c['program_length'] for c in data if c['solution_found']])/n_solved
    accuracy = sum(accuracies)/len(accuracies) * 100
    aggregate_data = {
        'n_cases': n_cases,
        'n_solved': n_solved,
        'exec_time': exec_time,
        'program_length': program_length,
        'accuracy': accuracy,
    }
    name_aggregate[name] = aggregate_data
    print()
    print(sum(accuracies)/len(accuracies))
    print(solutions_found/n_cases)

    # amount_fully_correct = len(list(filter(lambda a: a == 1.0, accuracies)))
    # print(amount_fully_correct/len(accuracies) * 100)
    # print(f"{name}: {n_solved}/{n_cases} {n_solved/n_cases*100} accuracy: {accuracy} exec_time: {exec_time} program_length: {program_length}")

#%%


def avg_prop_by_prop(data: list[dict], key, by_key, only_solved=False):
    result = {}
    for case in data:
        if only_solved and case['solution_found'] == False:
            continue
        by_prop = case[by_key]
        result[by_prop] = result.get(by_prop, []) + [case[key]]
    for by_prop in result:
        result[by_prop] = sum(result[by_prop]) / len(result[by_prop])
    return result

#%%


for name, data in name_data.items():
    size_accuracy = avg_prop_by_prop(data, 'accuracy', 'n1', only_solved=False)
    plt.plot(size_accuracy.keys(), size_accuracy.values(), "o-", label=name)

plt.legend()
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

def plot_aggregate(xprop, yprop):
    for name, data in name_aggregate.items():
        plt.scatter(data[xprop], data[yprop], label=name)
        plt.annotate(name, (data[xprop], data[yprop]))
    plt.xlabel(xprop)
    plt.ylabel(yprop)

#%%

plot_aggregate('exec_time', 'accuracy')
plt.tight_layout()
plt.show()

#%%

plot_aggregate('program_length', 'accuracy')
plt.tight_layout()
plt.show()
