from typing import List, Tuple

from common.prorgam import Program


class SearchResult:

    def __init__(
            self,
            program: Program,
            process_time_sec: float,
            number_of_explored_programs: int,
            cost_per_iteration: List[Tuple[int, float]],
            number_of_iterations: int
    ):
        self.dictionary = {
            'program': program,
            'program_length': program.number_of_tokens(),
            'execution_time': process_time_sec,
            'number_of_explored_programs': number_of_explored_programs,
            'cost_per_iteration': cost_per_iteration,
            'number_of_iterations': number_of_iterations,
        }
