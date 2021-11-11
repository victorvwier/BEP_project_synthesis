from brute_search import *

def test_extend_program():
    P1 = Program([MoveDown(), MoveRight()])
    P2 = Program([MoveUp(), MoveLeft()])
    P3 = Program([MoveDown(), MoveUp()])
    updated_programs = extend_program(P1, [P1, P2, P3])
    print_ps(updated_programs)

def test_find_best_program():
    P1 = Program([MoveDown(), Draw()])
    P2 = Program([MoveRight(), MoveLeft()])
    P3 = Program([MoveDown(), MoveRight(), Draw()])
    start_state = PixelEnvironment(2, 0, 0, [[False, False], [False, False]])
    end_state = PixelEnvironment(2, 1, 1, [[False, False], [False, True]])
    best_program, _, solved = find_best_program([P1, P2, P3], [start_state], [end_state])
    print_p(best_program)
    print(solved)

def test_search():
    tokens = [MoveDown(), MoveRight(), Draw()]
    start_state = PixelEnvironment(2, 0, 0, [[False, False], [False, False]])
    end_state = PixelEnvironment(2, 1, 1, [[False, False], [False, True]])
    num_iterations = 3
    best_program, _, solved = search(tokens, [(start_state, end_state)], num_iterations)
    print_p(best_program)
    print(solved)


# test_extend_program()
# test_find_best_program()
# test_search()