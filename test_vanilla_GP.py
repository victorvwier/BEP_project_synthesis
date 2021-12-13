from common.experiment import Example
from common.prorgam import Program
from common.tokens.control_tokens import If
from evaluation.experiment_procedure import extract_bool_tokens_from_domain_name, extract_trans_tokens_from_domain_name, test_performance_single_experiment
from common.tokens.pixel_tokens import *
from example_parser.string_parser import StringParser
from search.gen_prog.vanilla_GP import VanillaGP

def test_gen_fitness():
    start_state = PixelEnvironment(2, 2, 0, 0, (False, False, False, False))
    end_state = PixelEnvironment(2, 2, 1, 1, (False, False, False, True))

    p1 = Program([If(AtRight(), [MoveDown()], [MoveLeft()]), If(AtRight(), [MoveRight()], [MoveRight()]), If(NotAtRight(), [Draw()], [MoveRight()])])
    p2 = Program([If(AtLeft(), [MoveRight()], [MoveDown()])])
    p3 = Program([If(AtBottom(), [MoveLeft()], [MoveRight()]), If(AtBottom(), [MoveUp()], [MoveLeft()]), If(NotAtBottom(), [MoveDown()], [Draw()])])
    p4 = Program([If(AtLeft(), [MoveRight()], [MoveLeft()]), MoveDown(), Draw()])
    programs = [p1, p2, p3] # does not sort correctly
    programs = [p1, p2, p3, p4] # does sort correctly with one extra element

    search_method = VanillaGP(10.0)
    search_method.seed = 26
    search_method.examples = [Example(start_state, end_state)]
    search_method.current_gen = programs

    [print(f, s, p) for f, s, p in search_method.gen_fitness()]

def test_one_point_crossover_even():
    p1 = Program([If(AtBottom(), [MoveLeft()], [MoveRight()]), If(AtBottom(), [MoveUp()], [MoveLeft()]), If(NotAtBottom(), [MoveDown()], [Draw()]), Draw()])
    p2 = Program([If(AtLeft(), [MoveRight()], [MoveLeft()]), MoveDown(), Draw(), MoveLeft()])
    print(p1)
    print(p2)
    print("-----------")

    search_method = VanillaGP(10.0)

    child_1, child_2 = search_method.one_point_crossover(p1, p2)

    print(child_1)
    print(child_2)
    print("-----------")
def test_one_point_crossover_odd():
    p1 = Program([If(AtBottom(), [MoveLeft()], [MoveRight()]), If(AtBottom(), [MoveUp()], [MoveLeft()]), If(NotAtBottom(), [MoveDown()], [Draw()])])
    p2 = Program([If(AtLeft(), [MoveRight()], [MoveLeft()]), MoveDown(), Draw(), MoveLeft(), MoveDown(), MoveUp()])
    print(p1)
    print(p2)
    print("-----------")

    search_method = VanillaGP(10.0)

    child_1, child_2 = search_method.one_point_crossover(p1, p2)

    print(child_1)
    print(child_2)
    print("-----------")
def test_n_point_crossover():
    p1 = Program([If(AtBottom(), [MoveLeft()], [MoveRight()]), If(AtBottom(), [MoveUp()], [MoveLeft()]), If(NotAtBottom(), [MoveDown()], [Draw()])])
    p2 = Program([If(AtLeft(), [MoveRight()], [MoveLeft()]), MoveDown(), Draw(), MoveLeft(), MoveDown(), MoveUp()])
    print(p1)
    print(p2)
    print("-----------")

    search_method = VanillaGP(10.0)

    child_1, child_2 = search_method.n_point_crossover(1, p1, p2, [1], [3])

    print(child_1)
    print(child_2)
    print("-----------")

def test_vanillaGP():
    trans_tokens = extract_trans_tokens_from_domain_name("pixel")
    bool_tokens = extract_bool_tokens_from_domain_name("pixel")
    start_state = PixelEnvironment(2, 2, 0, 0, (False, False, False, False))
    end_state = PixelEnvironment(2, 2, 1, 1, (False, False, False, True))
    # for i in range(0, 51):
    #     search_method = VanillaGP(10.0)
    #     search_method.seed = i
    #     print("seed =", search_method.seed)
    #     search_result = search_method.run([Example(start_state, end_state)], trans_tokens, bool_tokens)
    #     print(search_result.dictionary)
    #     print(search_result.dictionary["program"])
    search_method = VanillaGP(10.0)
    search_result = search_method.run([Example(start_state, end_state)], trans_tokens, bool_tokens)
    print(search_result.dictionary)
    print(search_result.dictionary["program"])


def test_on_actual_experiment():
    vanillaGP = VanillaGP
    experiment = StringParser().parse_specific_range(
        range(0, 10), range(0, 10), range(0, 10))
    (ave_suc, ave_time, com_suc) = test_performance_single_experiment(
        experiment, vanillaGP)

# test_gen_fitness()
# test_one_point_crossover_even()
# test_one_point_crossover_odd()
# test_n_point_crossover()

# test_vanillaGP()
test_on_actual_experiment()