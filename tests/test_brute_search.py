from common.experiment import Example
from common.prorgam import Program
from common.tokens.pixel_tokens import *
from search.brute.brute import extend_program, print_ps, Brute, print_p


def test_extend_program():
    P1 = Program([MoveDown(), MoveRight()])
    P2 = Program([MoveUp(), MoveLeft()])
    P3 = Program([MoveDown(), MoveUp()])
    updated_programs = extend_program(P1, [P1, P2, P3])
    print_ps(updated_programs)


def test_search():
    tokens = {MoveDown, MoveRight, Draw}
    start_state = PixelEnvironment(2, 2, 0, 0, [[False, False], [False, False]])
    end_state = PixelEnvironment(2, 2, 1, 1, [[False, False], [False, True]])
    num_iterations = 3
    best_program, _, solved = Brute(10).run([Example(start_state, end_state)], tokens, set())
    print_p(best_program)
    print(solved)

# test_extend_program()
# test_find_best_program()
# test_search()
