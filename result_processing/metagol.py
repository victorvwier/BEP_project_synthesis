from result_processing.result_parser import Results


def run():
    colors = {
        "metagol": "xkcd:tomato",
    }

    data = [{"name": "metagol", "file": "../results/Metagol/metagol2.txt"}]

    complexity = "#examples"

    # Complexity vs accuracy
    results = Results(data, colors)
    results.filter("test_total", lambda t: t > 0)
    results.filter_fields(["complexity", "test_acc"])
    results.aggregate("complexity")
    results.plot(
        x=lambda t: t[0],
        y=lambda t: t[1]["test_acc"]*100,
        title="{} vs accuracy".format(complexity),
        x_axis=complexity,
        y_axis="Accuracy (% correct)"
    )
    results.save(1, "S", "metagol")


if __name__ == "__main__":
    run()