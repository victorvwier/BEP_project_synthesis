from common_environment.environment import Environment, RobotEnvironment
from experiment_procedure import Example, TestCase
from robot_environment import robot_tokens
import re

class Parser():
    def parse(filename: str) -> TestCase:
        raise NotImplementedError()

# Parses a single file containing a test case for the Robot
class RobotParser():
    def parseEnvironment(data: 'list[str]') -> Environment:
        return RobotEnvironment(data[5], data[0], data[1], data[2], data[3], data[4] == "0")            

    def parse(filename: str) -> TestCase:
        # open the file
        f = open(filename, 'r')

        # construct examples from the input
        data = f.read()
        regex = re.compile(r"\([^)]*\)")
        in_out = regex.findall(data)
        in_out[0] = in_out[0][2::]
        
        # split 
        in_data = in_out[0][1:-1].split(",")
        out_data = in_out[1][1:-1].split(",")

        in_env = [RobotParser.parseEnvironment(in_data)]
        out_env = [RobotParser.parseEnvironment(out_data)]
        ex = Example(in_env, out_env)    

        TestCase(ex, ex, robot_tokens.TransTokens, robot_tokens.BoolTokens)


if __name__ == "__main__":
    rp = RobotParser()
    RobotParser.parse("programs/e1-robots/data/2-0-0.pl")



    