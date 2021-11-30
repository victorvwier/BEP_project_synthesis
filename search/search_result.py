from common.prorgam import Program


class SearchResult:

    def __init__(self, program: Program, process_time_sec: float):        
        self.dictionary = {
            'program': program,
            'program_length': program.number_of_tokens(),
            'execution_time': process_time_sec,
        }
    