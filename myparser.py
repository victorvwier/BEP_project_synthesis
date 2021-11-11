from typing import List, Tuple
from common_environment.environment import Environment, PixelEnvironment, RobotEnvironment, StringEnvironment
import re
from os import walk
from os import listdir
from os.path import isfile, join

class Example:
    def __init__(self, input_environment: Environment, output_environment: Environment):
        self.input_environment = input_environment
        self.output_environment = output_environment

class TestCase:
    def __init__(self, training_examples: List[Example], test_examples: List[Example]):
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
class RobotParser():
    def parse(filename: str) -> TestCase:
        # open the file
        f = open(filename, 'r')

        # construct examples from the input
        data = f.read()
        regex = re.compile("\([^w]([^)]+?)\)")
        for p in regex.findall(data):
            print(p)

class StringParser():
        

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

        test_case = TestCase(training_examples, test_examples)
        return test_case

    
    def parse_single_example_file(file_name) -> List[Example]: 
        file = open(file_name, "r")
        lines = file.readlines()
        
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


    def parse_single_example_file(file_name) -> List[Example]: 
        file = open(file_name, "r")
        lines = file.readlines()
        
        examples = []
        for line in lines:
            examples.append(StringParser.parse_single_line(line))
    
    





# if __name__ == "__main__":
#     rp = RobotParser()
#     RobotParser.parse("programs/e1-robots/data/2-0-0.pl")
#     StringParser.parse_single_example_file("programs/e2-strings/data/test/1-222-10.pl")


    