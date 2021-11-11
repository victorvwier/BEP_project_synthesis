from os import X_OK
from common_environment.environment import Environment, PixelEnvironment, RobotEnvironment, StringEnvironment
from robot_environment import robot_tokens
from pixel_environment import pixel_tokens
import re
from typing import List, Tuple
from os import walk
from os import listdir
from os.path import isfile, join

class Example:
    def __init__(self, input_environment: Environment, output_environment: Environment):
        self.input_environment = input_environment
        self.output_environment = output_environment

class TestCase:
    def __init__(self, file_name: str, training_examples: List[Example], test_examples: List[Example]):
        self.file_name = file_name
        self.training_examples = training_examples # tuple consisting of input environment and wanted output environment
        self.test_examples = test_examples  # tuple consisting of input environment and wanted output environment



class Experiment:
    def __init__(self, name: str, domain_name: str, test_cases: List[TestCase]):
        self.name = name
        self.domain_name = domain_name
        self.test_cases = test_cases
    def __str__(self):
        return "Experiment: " + self.name + "<TestCases: " + str(self.test_cases) + ">"

    def __repr__(self):
        return "Experiment: " + self.name + "<TestCases: " + str(self.test_cases) + ">"

class Parser():
    def parse(filename: str) -> TestCase:
        raise NotImplementedError()
    
    def openFile(filename: str) -> str:
        f = open(filename, 'r')
        data = f.read()
        return data

    def extract_domain_from_environment(environment):
        domain_name = "unknown"
        if isinstance(environment, RobotEnvironment): 
            domain_name = "robot"
        elif isinstance(environment, StringEnvironment): 
            domain_name = "string"
        elif isinstance(environment, PixelEnvironment): 
            domain_name = "pixel"
        return domain_name


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

        TestCase([ex], [ex], robot_tokens.TransTokens, robot_tokens.BoolTokens)

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
                pixels[x][y] = pixeldata[x*width + y] == '1'

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
        return TestCase(filename, [ex], [ex])

class StringParser():
        
    @staticmethod
    def get_all_string_experiments():

        # get list of all filenames in "programs/e2-strings/data/test" directory
        filenames1 = [f for f in listdir("programs/e2-strings/data/test") if isfile(join("programs/e2-strings/data/test", f))]

        experiment_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        experiment_tuple_lists: List[List[Tuple[str, str]]]= []
        experiments: List[Experiment] = []
        for _ in range(len(experiment_names)):
            experiment_tuple_lists.append([])
            experiments.append([])

        for file_name in filenames1:

            for i, name in enumerate(experiment_names):
                if (name == file_name[0]):
                    training_file_name = "programs/e2-strings/data/train/" + file_name
                    testing_file_name = "programs/e2-strings/data/test/" + file_name
                    experiment_tuple = (training_file_name, testing_file_name)
                    experiment_tuple_lists[i].append(experiment_tuple)

        for i, name in enumerate(experiment_names):
            experiment = StringParser.parse_experiment(experiment_tuple_lists[i], name)
            experiments[i] = experiment
        
        return experiments
        

    def parse_experiment(file_names_tuples: List[Tuple[str, str]], experiment_name_extention):
        
        test_cases: List[TestCase] = []
        
        for tuple in file_names_tuples:
            training_file_name = tuple[0]
            test_file_name = tuple[1]
            test_case = StringParser.parse_test_case(training_file_name, test_file_name)
            test_cases.append(test_case)

        domain_name = "string"
        experiment = Experiment("String experiments: " + experiment_name_extention, domain_name, test_cases)
        return experiment

        
        

    def parse_test_case(file_name_training_data, file_name_test_data = None) -> TestCase:
        
        # if no test_data is given, use training_data as test_data
        if (file_name_training_data == None):
            file_name_test_data = file_name_training_data
        
        training_examples = StringParser.parse_single_example_file(file_name_training_data)
        test_examples = StringParser.parse_single_example_file(file_name_test_data)

        test_case = TestCase(file_name_training_data.split("/")[-1] , training_examples, test_examples)
        return test_case

    
    def parse_single_example_file(file_name) -> List[Example]: 
        file = open(file_name, "r")
        lines = file.readlines()

        # print(file_name)
        
        examples = []
        for line in lines:
            examples.append(StringParser.parse_single_line(line))
    
    # def parse(filename_traindata: str, filename_testdata) -> TestCase:
    def parse_single_line(line: str) -> Example:
        _, temp = line.split("pos(w(")
        input_data, output_data = temp.split(",w(")

        # correct the start possition, since the data seems to use index 1 as first index instead of index 0
        start_pos = int(input_data.split(",")[0])
        if start_pos > 0:
            start_pos -= 1

        
        input_string = StringParser.extract_string(input_data)
        output_string = StringParser.extract_string(output_data)

        input_environment = StringEnvironment(input_string, start_pos)
        output_environment = StringEnvironment(output_string)

        example = Example(input_environment, output_environment)
        return example



    # extracts the string which is represented in part of the data
    # input example: "1,6,['@','h','a','r','r','y'])"
    # output example: "@harry"
    def extract_string(data: str) -> str:
        
        # get an array of strings, each containing a presentation of a character
        # e.g. ["'@'", "'h'", "'a'", "'r'", "'r'", "'y'"]
        string_array = data.split("[")[1].split("]")[0].split(",")
        
        # remove the "\'" characters from each string 
        # e.g. ['@', 'h', 'a', 'r', 'r', 'y']
        string_array = list(map(lambda string: string.replace("\'", ""), string_array))
        
        # combine all characters in the list to form a string 
        string = ""
        for char in string_array:
            string += char
        return string

    # def parse_single_example_file(file_name) -> List[Example]: 
    #     file = open(file_name, "r")
    #     lines = file.readlines()
        


    #     examples = []
    #     for line in lines:
    #         examples.append(StringParser.parse_single_line(line))
    
    

if __name__ == "__main__":
    PixelParse.parse("programs/e3-pixels/data/1-0-1.pl")



    