import unittest

from common.prorgam import Program
from common.tokens.string_tokens import *
from search.vlns.large_neighborhood_search.destroy.remove_n_destroy import ExtractNDestroy


class MyTestCase(unittest.TestCase):
    @staticmethod
    def pr(size: int):
        lib = [MoveLeft(), MoveRight(), MakeLowercase(), MakeUppercase(), Drop()]

        seq = []

        for i in range(size):
            seq.append(lib[i % 5])

        return Program(seq)

    def test_n_is_0(self):
        p = self.pr(5)

        r = ExtractNDestroy(p_extract=0.5, n_options=[0], n_weights=[1]).destroy(p)

        print(r)

    def test_n_is_1(self):
        p = self.pr(5)

        r = ExtractNDestroy(p_extract=0.2, n_options=[1], n_weights=[1]).destroy(p)

        print(r)

    def test_n_more_than_1(self):
        p = self.pr(5)

        r2 = ExtractNDestroy(p_extract=0.2, n_options=[2], n_weights=[1]).destroy(p)
        r3 = ExtractNDestroy(p_extract=0.2, n_options=[3], n_weights=[1]).destroy(p)
        r4 = ExtractNDestroy(p_extract=0.2, n_options=[4], n_weights=[1]).destroy(p)
        r5 = ExtractNDestroy(p_extract=0.2, n_options=[5], n_weights=[1]).destroy(p)

        print("N = 2: {}".format(r2))
        print("N = 3: {}".format(r3))
        print("N = 4: {}".format(r4))
        print("N = 5: {}".format(r5))

    def test_big_program(self):
        p = self.pr(100)

        r = ExtractNDestroy(p_extract=0.2, n_options=[2], n_weights=[1]).destroy(p)

        print(r)

    def test_weights(self):
        p = self.pr(10)

        r = ExtractNDestroy(p_extract=0.2, n_options=[0, 1, 2], n_weights=[3,2,1]).destroy(p)

        print(r)



if __name__ == '__main__':
    unittest.main()
