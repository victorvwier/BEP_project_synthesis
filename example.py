from parser import PixelParse

from experiment_procedure import test_performance_single_case


if __name__ == "__main__":
    testcase = PixelParse.parse("programs/e3-pixels/data/1-0-1.pl")
    (succesper, time) = test_performance_single_case(testcase)
    print("Test case worked for {}% of the time, running time: {}".format(succesper, time))
