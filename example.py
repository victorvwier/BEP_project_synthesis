from myparser import PixelParse

from experiment_procedure import test_performance_single_case
from pixel_environment import pixel_tokens

if __name__ == "__main__":
    testcase = PixelParse.parse("programs/e3-pixels/data/1-1-2.pl")
    (succesper, time) = test_performance_single_case(testcase, pixel_tokens.TransTokens, pixel_tokens.BoolTokens)
    print("Test case worked for {}% of the time, running time: {}".format(succesper, time))
