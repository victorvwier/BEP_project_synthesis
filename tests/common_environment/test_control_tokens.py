import unittest

from common_environment.control_tokens import *
from common_environment.environment import *
from interpreter.interpreter import Program
from string_environment.string_tokens import *


class TestIf(unittest.TestCase):
    def test_simple(self):
        e1 = StringEnvironment("Hello, World!")
        e2 = StringEnvironment("hello, World!")
        p = Program([
            If(IsUppercase(), [MakeLowercase()], [MakeUppercase()])
        ])

        e1 = p.interp(e1)
        e2 = p.interp(e2)

        self.assertEqual(e1.to_string(), "hello, World!")
        self.assertEqual(e2.to_string(), "Hello, World!")

    def test_nested(self):
        e1 = StringEnvironment("hello, World!")
        e2 = StringEnvironment("Hello, World!")
        e3 = StringEnvironment("#ello, World!")
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

    def test_equality(self):
        self.assertEqual(If(AtStart(), [MoveLeft(), MoveRight()], [Drop(), MoveRight()]),
                         If(AtStart(), [MoveLeft(), MoveRight()], [Drop(), MoveRight()]))
        self.assertNotEqual(If(AtEnd(), [MoveLeft(), MoveRight()], [Drop(), MoveRight()]),
                            If(AtStart(), [MoveLeft(), MoveRight()], [Drop(), MoveRight()]))
        self.assertNotEqual(If(AtStart(), [MoveLeft(), MoveLeft()], [Drop(), MoveRight()]),
                            If(AtStart(), [MoveLeft(), MoveRight()], [Drop(), MoveRight()]))


class TestRecurse(unittest.TestCase):
    def test_simple(self):
        e1 = StringEnvironment("hello, world!")
        p = Program([
            Recurse(NotAtEnd(), [MakeUppercase()], [MakeUppercase(), MoveRight()])
        ])

        e1 = p.interp(e1)
        self.assertEqual(e1.to_string(), "HELLO, WORLD!")

    def test_limit(self):
        e1 = StringEnvironment("hello, world!")
        p = Program([
            Recurse(NotAtEnd(), [], [])
        ])

        self.assertRaises(RecursiveCallLimitReached, lambda : p.interp(e1))

    def test_equality(self):
        self.assertEqual(Recurse(AtStart(), [MoveLeft(), MoveRight()], [Drop(), MoveRight()]),
                         Recurse(AtStart(), [MoveLeft(), MoveRight()], [Drop(), MoveRight()]))
        self.assertNotEqual(Recurse(AtEnd(), [MoveLeft(), MoveRight()], [Drop(), MoveRight()]),
                            Recurse(AtStart(), [MoveLeft(), MoveRight()], [Drop(), MoveRight()]))
        self.assertNotEqual(Recurse(AtStart(), [MoveLeft(), MoveLeft()], [Drop(), MoveRight()]),
                            Recurse(AtStart(), [MoveLeft(), MoveRight()], [Drop(), MoveRight()]))



class TestLoop(unittest.TestCase):
    def test_simple(self):
        e1 = StringEnvironment("hello, world!")
        p = Program([
            LoopWhile(NotAtEnd(), [MakeUppercase(), MoveRight()]),
            MakeUppercase()
        ])

        e1 = p.interp(e1)
        self.assertEqual(e1.to_string(), "HELLO, WORLD!")

    def test_limit(self):
        e1 = StringEnvironment("hello, world!")
        p = Program([
            LoopWhile(NotAtEnd(), [])
        ])

        self.assertRaises(LoopIterationLimitReached, lambda : p.interp(e1))

    def test_equality(self):
        self.assertEqual(LoopWhile(AtStart(), [MoveLeft(), MoveRight()]),
                         LoopWhile(AtStart(), [MoveLeft(), MoveRight()]))
        self.assertNotEqual(LoopWhile(AtEnd(), [MoveLeft(), MoveRight()]),
                            LoopWhile(AtStart(), [MoveLeft(), MoveRight()]))
        self.assertNotEqual(LoopWhile(AtStart(), [MoveLeft(), MoveLeft()]),
                            LoopWhile(AtStart(), [MoveLeft(), MoveRight()]))

if __name__ == '__main__':
    unittest.main()
