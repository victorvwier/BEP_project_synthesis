from common_environment.environment import Environment
from experiment_procedure import Example, TestCase
import re

class Parser():
    def parse(filename: str) -> TestCase:
        raise NotImplementedError()

# Parses a single file containing a test case for the Robot
class RobotParser():
    def parse(filename: str) -> TestCase:
        # open the file
        f = open(filename, 'r')

        # construct examples from the input
        data = f.read()
        regex = re.compile("\([^w]([^)]+?)\)")
        for p in regex.findall(data):
            print(p)

if __name__ == "__main__":
    rp = RobotParser()
    RobotParser.parse("programs/e1-robots/data/2-0-0.pl")


    