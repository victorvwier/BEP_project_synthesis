from parser import PixelParse

from experiment_procedure import test_performance_single_case


if __name__ == "__main__":
    testcase = PixelParse.parse("programs/e3-pixels/data/0-0-1.pl")
    test_performance_single_case(testcase)
