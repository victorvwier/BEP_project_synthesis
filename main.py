from search.batch_run import BatchRun
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n import RemoveNInsertN

if __name__ == "__main__":
    result = BatchRun(
        # Task domain
        domain="robot",

        # Iterables for files name. Use [] to use all values.
        # This runs all files adhering to format "2-*-[0 -> 10]"
        # Thus, ([], [], []) runs all files for a domain.
        files=([2], [], range(0, 11)),

        search_algorithm=RemoveNInsertN(),

        # Name is used for storing files
        algorithm_name="VLNS",

        # Prints out result when test_case is finished
        print_results=True,
    ).run()
