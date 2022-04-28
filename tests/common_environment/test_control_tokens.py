import unittest

from common.tokens.control_tokens import *
from common.program import Program
from common.tokens.string_tokens import *


class TestIf(unittest.TestCase):
    def test_simple(self):
        e1 = StringEnvironment(list("Hello, World!"))
        e2 = StringEnvironment(list("hello, World!"))
        p = Program([
            If(IsUppercase(), [MakeLowercase()], [MakeUppercase()])
        ])

        e1 = p.interp(e1)
        e2 = p.interp(e2)

        self.assertEqual(e1.to_string(), "hello, World!")
        self.assertEqual(e2.to_string(), "Hello, World!")

    def test_nested(self):
        e1 = StringEnvironment(list("hello, World!"))
        e2 = StringEnvironment(list("Hello, World!"))
        e3 = StringEnvironment(list("#ello, World!"))
        p = Program([
            If(IsUppercase(),
               [MakeLowercase()],
               [If(IsLowercase(),
                   [MakeUppercase()],
                   [Drop()]
                   )])
        ])

        e1 = p.interp(e1)
        e2 = p.interp(e2)
        e3 = p.interp(e3)

        self.assertEqual(e1.to_string(), "Hello, World!")
        self.assertEqual(e2.to_string(), "hello, World!")
        self.assertEqual(e3.to_string(), "ello, World!")

class TestLoop(unittest.TestCase):
    def test_simple(self):
        e1 = StringEnvironment(list("hello, world!"))
        p = Program([
            LoopWhile(NotAtEnd(), [MakeUppercase(), MoveRight()]),
            MakeUppercase()
        ])

        e1 = p.interp(e1)
        self.assertEqual(e1.to_string(), "HELLO, WORLD!")

    def test_limit(self):
        e1 = StringEnvironment(list("hello, world!"))
        p = Program([
            LoopWhile(NotAtEnd(), [])
        ])

        self.assertRaises(LoopIterationLimitReached, lambda : p.interp(e1))

if __name__ == '__main__':
    unittest.main()
