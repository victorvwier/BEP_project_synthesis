from os import X_OK
from common_environment.environment import Environment, PixelEnvironment, RobotEnvironment
from experiment_procedure import Example, TestCase
from robot_environment import robot_tokens
from pixel_environment import pixel_tokens
import re

class Parser():
    def parse(filename: str) -> TestCase:
        raise NotImplementedError()
    
    def openFile(filename: str) -> str:
        f = open(filename, 'r')
        data = f.read()
        return data

# Parses a single file containing a test case for the Robot
class RobotParser(Parser):
    PATH = "programs/e1-robots/data/"
    def parseEnvironment(data: 'list[str]') -> Environment:
        return RobotEnvironment(data[5], data[0], data[1], data[2], data[3], data[4] == "0")            

    def parse(filename: str) -> TestCase:
        data = Parser.openFile(filename)
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

class PixelParse(Parser):
    PATH = "programs/e3-pixels/data/"
    def parseEnvironment(data:str) -> Environment:
        tokens = data.split(',')
        x = tokens[0]
        y = tokens[1]
        width = int(tokens[2])
        height = int(tokens[3])

        if(x == '_'):
            x = 0
        else:
            x = int(x)

        if(y == '_'):
            y = 0
        else:
            y = int(y)

        pixeldata = ''.join(''.join(tokens[4::])[1:-1].split(' ')) ## converts {'[0',' 0',' 0',' 0',' 0',' 1']} into 000001
        pixels = [[False for _ in range(height)] for _ in range(width)]
        
        for x in range(0, width):
            for y in range(0, height):
                pixels[x][y] = pixeldata[x*width + y]

        return PixelEnvironment(int(width),int(height), int(x),int(y), pixels)

    def parse(filename:str) -> TestCase:
        data = Parser.openFile(filename)
        regex = re.compile(r"\([^)]*\)")

        in_out = regex.findall(data)
        in_out[0] = in_out[0][2::]

        # split
        in_data = in_out[0][1:-1]
        out_data = in_out[1][1:-1]

        in_env = PixelParse.parseEnvironment(in_data)
        out_env = PixelParse.parseEnvironment(out_data)

        ex = Example(in_env, out_env)    
        return TestCase([ex], [ex], pixel_tokens.TransTokens, pixel_tokens.BoolTokens)


if __name__ == "__main__":
    PixelParse.parse("programs/e3-pixels/data/1-0-1.pl")



    