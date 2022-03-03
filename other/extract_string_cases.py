from example_parser.string_parser import StringParser


def separator_predictions(ex):
    inp = ex.input_environment.string_array
    out = ex.output_environment.string_array

    removed = {}

    for char in inp:
        if char not in removed:
            removed[char] = 0

        removed[char] += 1

    for char in out:
        if char not in removed:
            removed[char] = 0

        removed[char] -= 1

    removed = [(k, v) for k, v in removed.items()]
    removed.sort(key=lambda p: -p[1])
    return [p[0] for p in removed if not (p[0].isalpha() or p[0].isnumeric())]

if __name__ == "__main__":
    parser = StringParser()
    cases = parser.parse_specific_range([1], [], [1])

    for case in cases:
        ex = case.training_examples[0]

        case = case.index[1]
        inp = ex.input_environment.to_string()
        exp = ex.output_environment.to_string()
        sp = separator_predictions(ex)

        print("{}\t{}\t{}\t{}".format(case, inp, exp, sp))
