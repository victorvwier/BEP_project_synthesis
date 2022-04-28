from common.environment.environment import Environment


class Example:
    """An Example exists of an input Environment and a desired output Environment."""

    def __init__(self, input_environment: Environment, output_environment: Environment):
        self.input_environment = input_environment
        self.output_environment = output_environment


class TestCase:
    """A TestCase exists of a list of training and test Examples."""

    def __init__(self, training_examples: 'list[Example]', test_examples: 'list[Example]',
                 index: (int, int, int)):
        self.training_examples = training_examples  # tuple consisting of input environment and wanted output environment
        self.test_examples = test_examples  # tuple consisting of input environment and wanted output environment

        self.index = index

    def state(self, input_env = True, training = True) -> tuple:
        cases = self.training_examples if training else self.test_examples

        if input_env:
            return tuple([tc.input_environment for tc in cases])

        return tuple([tc.output_environment for tc in cases])

class Experiment:
    """An Experiment consists of a list of TestCases, a name for the Expirement and the name of the domain."""

    def __init__(self, name: str, domain_name: str, test_cases: 'list[TestCase]'):
        self.name = name
        self.domain_name = domain_name
        self.test_cases = test_cases

    def __str__(self):
        return "Experiment: " + self.name + "<TestCases: " + str(self.test_cases) + ">"

    def __repr__(self):
        return "Experiment: " + self.name + "<TestCases: " + str(self.test_cases) + ">"
