import json
from matplotlib import pyplot as plt

plt.rcParams["figure.dpi"] = plt.rcParamsDefault["figure.dpi"]
plt.rcParams["figure.figsize"] = (3, 3)

#%%
name_fname = {
    "brute":  "/tmp/pycharm_project_46/results/string/Brute-extra.txt",
    "astar":  "/tmp/pycharm_project_46/results/string/Astar-extra.txt",
    # "max":  "/tmp/pycharm_project_46/results/string/Astar-max.txt",
    # "min":  "results/string/Astar-min.txt",
    # "mean": "results/string/Astar-mean.txt",
    # "max-align": "results/string/Astar-max-alignment.txt",
    # "min-align": "results/string/Astar-min-alignment.txt",
    # "mean-align": "results/string/Astar-mean-alignment.txt",
}
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
    # for case in data:
    #     solution_found = data['solution_found']
    #     execution_time = data['execution_time']
    #     number_of_explored_programs = data['number_of_explored_programs']
    #     program_length = data['program_length']
    accuracies = []
    for case in data:
        n_examples = case['train_amount'] + case['test_amount']
        n_correct = case['train_amount_correct'] + case['test_amount_correct']
        accuracy = n_correct/n_examples
        accuracies.append(accuracy)

    n_cases = len(data)
    n_solved = sum([int(c['solution_found']) for c in data])
    exec_time = sum([c['execution_time'] for c in data if c['solution_found']])/n_solved
    program_length = sum([c['program_length'] for c in data if c['solution_found']])/n_solved
    accuracy = sum(accuracies)/len(accuracies) * 100
    print(f"{name}: {n_solved}/{n_cases} {n_solved/n_cases*100} accuracy: {accuracy} exec_time: {exec_time} program_length: {program_length}")


