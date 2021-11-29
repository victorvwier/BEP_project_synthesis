from math import exp

from interpreter.interpreter import Program
from parser.experiment import TestCase, Example


class Cost:

    def cost(self, program: Program, test_case: TestCase):
        return sum([Cost._cost_example(program, ex) for ex in test_case.test_examples])

    @staticmethod
    def _cost_example(program: Program, example: Example):
        try:
            res = program.interp(example.input_environment)
            return res.distance(example.output_environment)
        except:
            return float('inf')


class CostWithProgramLength(Cost):

    def __init__(self, f_inout: float, f_length: float):
        super().__init__()
        self.f_inout = f_inout
        self.f_length = f_length

    def cost(self, program: Program, test_case: TestCase):
        cost_inout = 1 - exp(-super().cost(program, test_case))
        cost_length = 1 - exp(-program.number_of_tokens())

        print("-=-=-=-")
        print(cost_inout)
        print(cost_length)

        return cost_inout * self.f_inout + cost_length * self.f_length
