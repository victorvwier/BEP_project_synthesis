import math
from common.experiment import Example
from common.prorgam import Program
from common.tokens.control_tokens import If
from evaluation.experiment_procedure import extract_bool_tokens_from_domain_name, extract_trans_tokens_from_domain_name, test_performance_single_experiment
# from common.tokens.pixel_tokens import *
from common.tokens.robot_tokens import *
# from example_parser.string_parser import StringParser
from search.batch_run import BatchRun
from search.brute.brute import Brute, evaluate_program
from search.gen_prog.vanilla_GP import VanillaGP, chose_with_prob, draw_from, normalize_fitness

def test_normalize_errors():
    errors = [0.3, 0.25, 0.05, float('inf')]
    print(errors)
    print(normalize_fitness(errors))

def test_chose_with_prob():
    chosen = True
    for i in range(0, 1000):
        print(chose_with_prob(0.5))

def test_program_fitness_1():
    # robot-2-1-9
    start = RobotEnvironment(2, 1, 0, 1, 1, holding=False)
    end = RobotEnvironment(2, 1, 1, 1, 1, holding=True)
    program = Program([MoveDown(), Grab()])

    vanillaGP = VanillaGP(10)
    vanillaGP.setup([Example(start, end)], TransTokens, BoolTokens)
    print(vanillaGP.program_fitness(program))

    brute = Brute(10)
    print(evaluate_program(program, [start], [end]))

    # seem to be the same
def test_program_fitness_2():
    # robot-2-1-9
    start = RobotEnvironment(2, 1, 0, 1, 1, holding=False)
    end = RobotEnvironment(2, 1, 1, 1, 1, holding=True)
    program = Program([If(AtLeft(), [MoveRight()], [MoveDown()])])

    brute = Brute(10)
    print(evaluate_program(program, [start], [end]))

    vanillaGP = VanillaGP(10)
    vanillaGP.setup([Example(start, end)], TransTokens, BoolTokens)
    print(vanillaGP.program_fitness(program))

    # seem to be the same


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
    search_method.training_examples = [Example(start_state, end_state)]
    search_method.current_gen = programs

    [print(f, s, p) for f, s, p in search_method.gen_fitness()]

def test_one_point_crossover():
    Px = Program([MoveLeft(), MoveRight(), MoveDown(), Grab(), MoveRight(), Drop()])
    Py = Program([MoveRight(), Grab(), [MoveRight(), MoveDown()], MoveLeft(), Drop(), MoveDown()])
    print(Px)
    print(Py)
    print("-----------")

    search_method = VanillaGP(10.0)

    child_x, child_y = search_method.one_point_crossover(Px, Py)

    print(child_x)
    print(child_y)
    print("-----------")
def test_n_point_crossover():
    Px = Program([MoveLeft(), MoveRight(), MoveDown(), Grab(), MoveRight(), Drop()])
    Py = Program([MoveRight(), Grab(), [MoveRight(), MoveDown()], MoveLeft(), Drop(), MoveDown()])
    print(Px)
    print(Py)
    print("-----------")

    search_method = VanillaGP(10.0)

    child_x, child_y = search_method.n_point_crossover(Px, Py)

    print(child_x)
    print(child_y)
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

def test_vanillaGP_robot():
    trans_tokens = extract_trans_tokens_from_domain_name("robot")
    bool_tokens = extract_bool_tokens_from_domain_name("robot")
    start_state = RobotEnvironment(6, 4, 3, 1, 1)
    end_state = RobotEnvironment(6, 1, 3, 6, 6)
    search_method = VanillaGP(10.0)
    search_result = search_method.run([Example(start_state, end_state)], trans_tokens, bool_tokens)
    print(search_result.dictionary)
    print(search_result.dictionary["program"])

def test_on_actual_experiment():
    # BatchRun(domain="robot", files=([2],[1],[9]), search_algorithm=Brute(10), print_results=True, multi_core=False).run()
    # vanillaGP.seed = 3
    # BatchRun(domain="robot", files=([2],[1],[9]), search_algorithm=VanillaGP(10), print_results=True, multi_core=False).run()
    BatchRun(domain="robot", files=([10],[2],[3]), search_algorithm=VanillaGP(60), print_results=True, multi_core=False).run()
    
# test_normalize_errors()
# test_chose_with_prob()

# test_gen_fitness()

# test_one_point_crossover()
# test_n_point_crossover()

# test_vanillaGP()
# test_vanillaGP_robot()
test_on_actual_experiment()