from search.a_star.a_star import AStar
from search.batch_run import BatchRun


if __name__ == "__main__":
    BatchRun(domain="string", files=([],[],[]), search_algorithm=AStar(10, weight='dynamic'), print_results=True, multi_core=True, outfile_suffix="").run()