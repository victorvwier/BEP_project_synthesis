from search.brute.brute import *

def print_programs(programs):
    for program in programs:
        print(program)

def test_extend_program():
    P1 = Program([MoveDown(), MoveRight()])
    P2 = Program([MoveUp(), MoveLeft()])
    P3 = Program([MoveDown(), MoveUp()])
    updated_programs = extend_program(P1, [P2, P3], [MoveDown(), MoveRight(), MoveUp(), MoveLeft()])
    print_programs(updated_programs)

def test__search():
    tokens = [MoveDown(), MoveRight(), Draw()]
    start_state = PixelEnvironment(2, 2, 0, 0, [[False, False], [False, False]])
    end_state = PixelEnvironment(2, 2, 1, 1, [[False, False], [False, True]])
    num_iterations = 3
    best_program, _, solved = _search(tokens, [Example(start_state, end_state)], num_iterations) # Why is _search not defined
    print(best_program)
    print(solved)


# test_extend_program()
# test__search()

# P1 = Program([MoveRight(), InventedToken([MoveLeft(), Draw()])])
# P2 = Program([MoveRight(), InventedToken([MoveLeft(), Draw()])])
# listP = [P1]
# listP = set(listP)
# listP.add(P2)
# print(listP)