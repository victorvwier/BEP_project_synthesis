import time
from statistics import mean

from common.settings.settings import Settings
from common.settings.string_levenshtein import StringLevenshtein
from common.settings.string_optimized_alignment import StringOptimizedAlignment
from common.program import Program, Token
from common.tokens.abstract_tokens import InvalidTransition
from common.experiment import TestCase, Example
from common.tokens.control_tokens import LoopIterationLimitReached, Environment
from solver.invent.invent import Invent
from solver.invent.static_invent import StaticInvent


class SearchAlgorithm:
    """Abstract interface for a program synthesis solver algorithm."""

    settings: Settings
    time_limit_sec: float
    debug: bool

    invent: Invent
    tokens: list[Token]

    training_examples: list[Example]
    input_state: tuple[Environment]
    test_examples: list[Example]

    empty_program_cost: float
    best_program: Program
    best_cost: float = float("inf")
    best_state: tuple[Environment]

    statistics: dict = {}

    def setup(self):
        """This method is called before a solver is performed. The solver will be performed for the given
        'training_examples'. Also the 'trans_tokens' and 'bool_tokens' that are available for the environment are given.
        """

        raise NotImplementedError()

    def iteration(self):
        """This method represents an iteration of the solver algorithm. This method will get called over and over
        again, as long as it returns True. It will stop whenever False is returned or a time limit is reached. The 
        solver will be performed for the given 'training_examples'. Also the 'trans_tokens' and 'bool_tokens' that are
        available for the environment are given."""

        raise NotImplementedError()

    def run(self, settings: Settings, time_limit_sec: float, debug: bool, test_case: TestCase) -> (Program, dict):
        """"Runs the solver method until a program is returned or the time limit is reached. First the setup method is
        called, followed by a repetition of the iteration method until either a result is obtained, or the time limit is
        reached"""
        start_time = time.process_time()

        # Reset String settings dictionary
        StringLevenshtein._map = {}
        StringOptimizedAlignment._map = {}

        # Common setup.
        self.settings = settings
        self.time_limit_sec = time_limit_sec
        self.debug = debug

        self.invent = StaticInvent()
        self.invent.setup(settings.trans_tokens, settings.bool_tokens)
        self.tokens = self.invent.perms + self.invent.loops + self.invent.ifs

        self.training_examples = test_case.training_examples
        self.input_state = tuple([t.input_environment for t in self.training_examples])
        self.test_examples = test_case.test_examples

        self.best_program = Program([])
        self.best_cost, self.best_state, _ = self.evaluate(self.best_program)
        self.empty_program_cost = self.best_cost

        self.statistics = {
            "complexity": test_case.index[0],
            "task": test_case.index[1],
            "trial": test_case.index[2],
            "no._explored_programs": 1,
            "best_cost_per_iteration": [(0, self.best_cost)],
            "no._iterations": 0,
        }

        self.setup()

        # self.iteration returns whether a new iteration should be performed. Break the loop if time limit reached.
        while self.iteration():
            self.statistics["no._iterations"] += 1

            if time.process_time() >= start_time + self.time_limit_sec:
                break

        run_time = time.process_time() - start_time

        self.statistics["execution_time"] = run_time
        self.statistics["best_program"] = str(self.best_program)
        self.statistics["test_cost"], _, self.statistics["test_correct"] = self.evaluate(self.best_program, train=False)
        self.statistics["train_cost"], _, self.statistics["train_correct"] = self.evaluate(self.best_program, train=True)
        self.statistics["test_total"] = len(self.test_examples)

        if self.debug:
            print(self.statistics)

        # Extend results and return.
        return self.best_program, self.statistics

    def evaluate(self, p: Program, train: bool = True):
        results = []
        costs = []
        correct_examples = 0

        examples = self.training_examples if train else self.test_examples

        for ex in examples:
            try:
                res = p.interp(ex.input_environment)
                cost = self.settings.distance(res, ex.output_environment)

                if cost == 0:
                    correct_examples += 1

            except (InvalidTransition, LoopIterationLimitReached):
                res = ""
                cost = float("inf")

            results.append(res)
            costs.append(cost)

        cost = mean(costs)

        if cost < self.best_cost:
            self.best_cost = cost
            self.best_program = p

            #self.statistics.get("best_cost_per_iteration", []).append((self.statistics.get("no._iterations", 1), self.best_cost))

        return cost, tuple(results), correct_examples

    def evaluate_state(self, state: tuple):
        costs = []

        for out, desired in zip(state, self.training_examples):
            cost = self.settings.distance(out, desired.output_environment)

            costs.append(cost)

        cost = mean(costs)

        if cost < self.best_cost:
            self.best_cost = cost

            #self.statistics["best_cost_per_iteration"].append((self.statistics["no._iterations"], self.best_cost))

        return cost

    def normalized_cost(self, state: tuple):
        costs = []
        n_costs = []

        for out, desired, inp in zip(state, self.training_examples, self.input_state):
            cost = self.settings.distance(out, desired.output_environment)
            costs.append(cost)

            if self.settings.domain == "string":
                div = len(desired.input_environment.string_array) + len(inp.string_array)
            elif self.settings.domain == "robot":
                div = 6 * desired.input_environment.size
            else:
                div = desired.input_environment.width * desired.input_environment.height

            if cost == float("inf"):
                n_cost = 1
            else:
                n_cost = cost / div

            assert 0 <= n_cost <= 1

            n_costs.append(n_cost)

        n_cost = mean(n_costs)
        cost = mean(costs)

        if cost < self.best_cost:
            self.best_cost = cost

            #self.statistics["best_cost_per_iteration"].append((self.statistics["no._iterations"], self.best_cost))

        return n_cost#, self.best_cost == cost
