from experiment_procedure import extract_trans_tokens_from_domain_name, extract_bool_tokens_from_domain_name
from interpreter.interpreter import Program
from invent import invent2
from parser.experiment import TestCase, Example
from vlns.large_neighborhood_search.cost import Cost


class ProgramSearch:

    def __init__(self, domain: str, max_token_function_depth: int, cost: Cost):
        env_tokens = extract_trans_tokens_from_domain_name(domain)
        bool_tokens = extract_bool_tokens_from_domain_name(domain)
        self.invented = invent2(env_tokens, bool_tokens, max_token_function_depth)

        self.cost = cost
        self.domain = domain

    def find(self, initial_solution: Program, test_case: TestCase) -> Program:
        raise NotImplementedError()
