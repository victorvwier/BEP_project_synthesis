from result_processing.result_parser import Results


def run(domain, setting, graph):
    colors = {
        "Brute": "xkcd:grey",
        "AS": "xkcd:chocolate",
        "GP": "xkcd:tomato",
        "LNS": "xkcd:orange",
        "MCTS": "xkcd:gold",
        "MH": "yellowgreen",
    }

    algorithms = ["Brute", "AS", "GP", "LNS", "MCTS", "MH"]
    #algorithms = ["Brute", "AS"]
    data = []
    for a in algorithms:
        data.append({"name": a, "file": "../results/{}/{}-{}{}-PC.txt".format(a, a, domain, setting)})

    complexity = {
        "R": "Grid size",
        "S": "#examples",
        "P": "Matrix size",
    }[domain]



# Complexity vs accuracy
    if graph == "compl_vs_acc":
        results = Results(data, colors)
        results.filter_fields(["complexity", "correct"])
        results.aggregate("complexity")
        results.plot(
            x=lambda t: t[0],
            y=lambda t: t[1]["correct"]*100,
            title="{} vs accuracy".format(complexity),
            x_axis=complexity,
            y_axis="Accuracy (% correct)"
        )
        results.save(1, domain, "complexity_vs_accuracy_{}-{}".format(domain, setting))

    if graph == "compl_vs_exe":
        results = Results(data, colors)
        results.filter("correct", lambda v: v == 1)
        # results.filter_all("file", "correct", lambda v: v == 1)
        results.filter_fields(["complexity", "execution_time"])
        results.aggregate("complexity")
        results.plot(
            x=lambda t: t[0],
            y=lambda t: t[1]["execution_time"],
            title="{} vs execution time of solved problems".format(complexity),
            x_axis=complexity,
            y_axis="Average execution time (sec)",
        )
        results.save(1, domain, "complexity_vs_execution_time_correct_{}-{}".format(domain, setting))

if __name__ == "__main__":

    run("P", "G", "compl_vs_acc")
    run("P", "G", "compl_vs_exe")


    """
    for domain in ["R", "P", "S"]:
        for setting in ["E", "G", "O"]:
            for graph in ["compl_vs_acc", "compl_vs_exe"]:
                try:
                    run(domain, setting, graph)
                except FileNotFoundError:
                    print(domain, setting)
    """