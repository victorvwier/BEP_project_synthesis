from unittest import TestCase

from common_environment.control_tokens import *
from interpreter.interpreter import Program
from string_environment.string_tokens import *
from common_environment.environment import StringEnvironment


class TestStringTransTokens(TestCase):
    def test_move_right(self):
        p1 = Program([MoveRight()])
        env = StringEnvironment("string")

        env = p1.interp(env)
        assert env.pos == 1

        env = p1.interp(env)
        assert env.pos == 2

        p2 = Program([MoveRight(), MoveRight(), MoveRight()])
        env = p2.interp(env)
        assert env.pos == 5

        self.assertRaises(InvalidTransition, lambda : p1.interp(env))

    def test_move_left(self):
        p1 = Program([MoveLeft()])
        env = StringEnvironment("string", pos = 5)

        env = p1.interp(env)
        assert env.pos == 4

        env = p1.interp(env)
        assert env.pos == 3

        p2 = Program([MoveLeft(), MoveLeft(), MoveLeft()])
        env = p2.interp(env)
        assert env.pos == 0

        self.assertRaises(InvalidTransition, lambda : p1.interp(env))

    def test_make_uppercase(self):
        p1 = Program([MakeUppercase(), MoveRight(), MoveRight(), MakeUppercase(), MoveRight(), MakeUppercase()])
        env = StringEnvironment("string")

        env = p1.interp(env)
        assert env.string_array == list("StRIng")

    def test_make_lowercase(self):
        p1 = Program([MakeLowercase(), MoveLeft(), MoveLeft(), MakeLowercase(), MoveLeft(), MakeLowercase()])
        env = StringEnvironment("STRING", pos = 5)

        env = p1.interp(env)
        assert env.string_array == list("STriNg")

    def test_drop(self):
        p1 = Program([MoveLeft(), Drop()])
        p2 = Program([MoveLeft(), Drop(), Drop()])
        env = StringEnvironment("string", pos=5)

        env = p1.interp(env)
        assert env.string_array == list("strig")
        assert env.pos == 4

        env = p2.interp(env)
        assert env.string_array == list("str")
        assert env.pos == 2

    def test_drop_all(self):
        p1 = Program([Drop()])
        ei = StringEnvironment("s")
        eo = StringEnvironment("")

        ei = p1.interp(ei)
        assert ei.correct(eo)

    def test_drop_empty(self):
        p = Program([Drop()])
        env = StringEnvironment("")

        self.assertRaises(InvalidTransition, lambda : p.interp(env))


class TestStringBoolTokens(TestCase):

    def test_at_end(self):
        p = Program([If(AtEnd(), [], [MoveRight()]), If(AtEnd(), [], [MoveRight()]), If(AtEnd(), [], [MoveRight()])])
        env = StringEnvironment("str", pos=0)

        env = p.interp(env)
        assert env.pos == 2

    def test_not_at_end(self):
        p = Program([LoopWhile(NotAtEnd(), [MoveRight()])])
        env = StringEnvironment("str", pos=0)

        env = p.interp(env)
        assert env.pos == 2

    def test_at_start(self):
        p = Program([If(AtStart(), [], [MoveLeft()]), If(AtStart(), [], [MoveLeft()]), If(AtStart(), [], [MoveLeft()])])
        env = StringEnvironment("str", pos=2)

        env = p.interp(env)
        assert env.pos == 0

    def test_not_at_start(self):
        p = Program([LoopWhile(NotAtStart(),[MoveLeft()])])
        env = StringEnvironment("str", pos=2)

        env = p.interp(env)
        assert env.pos == 0

    def test_is_letter(self):
        p = Program([If(IsLetter(), [Drop()], [MoveRight()]), Recurse(NotAtEnd(), [], [])])
        env = StringEnvironment("s1t2se3CK4cko5", pos=0)

        env = p.interp(env)
        assert env.to_string() == "12345"

    def test_is_not_letter(self):
        p = Program([If(IsNotLetter(), [Drop()], [MoveRight()]), Recurse(NotAtEnd(), [], [])])
        env = StringEnvironment("12s3t9ri398n5092g", pos=0)

        env = p.interp(env)
        assert env.to_string() == "string"

    def test_is_uppercase(self):
        p = Program([If(IsUppercase(), [MoveRight()], [Drop()]), Recurse(NotAtEnd(), [], [])])
        env = StringEnvironment("diSjdTjidRiqINjqG", pos=0)

        env = p.interp(env)
        assert env.to_string() == "STRING"

    def test_is_not_uppercase(self):
        p = Program([If(IsNotUppercase(), [Drop()], [MoveRight()]), Recurse(NotAtEnd(), [], [])])
        env = StringEnvironment("d489iSjdTjidRi13qINjqG", pos=0)

        env = p.interp(env)
        assert env.to_string() == "STRING"

    def test_is_lowercase(self):
        p = Program([If(IsLowercase(), [MoveRight()], [Drop()]), Recurse(NotAtEnd(), [], [])])
        env = StringEnvironment("12sRGM4tr34iNOKFn34g", pos=0)

        env = p.interp(env)
        assert env.to_string() == "string"

    def test_is_not_lowercase(self):
        p = Program([If(IsNotLowercase(), [Drop()], [MoveRight()]), Recurse(NotAtEnd(), [], [])])
        env = StringEnvironment("12sRGM4tr34iNOKFn34g", pos=0)

        env = p.interp(env)
        assert env.to_string() == "string"

    def test_is_number(self):
        p = Program([If(IsNumber(), [Drop()], [MoveRight()]), Recurse(NotAtEnd(), [], [])])
        env = StringEnvironment("1234s50t049r", pos=0)

        env = p.interp(env)
        assert env.to_string() == "str"

    def test_is_not_number(self):
        p = Program([If(IsNotNumber(), [Drop()], [MoveRight()]), Recurse(NotAtEnd(), [], [])])
        env = StringEnvironment("ha@1j2^&*3", pos=0)

        env = p.interp(env)
        assert env.to_string() == "123"

    def test_is_space(self):
        p = Program([If(IsSpace(), [Drop()], [MoveRight()]), LoopWhile(NotAtEnd(), [])])
        env = StringEnvironment("s t r i n g", pos=0)

        env = p.interp(env)
        assert env.to_string() == "string"

    def test_is_not_space(self):
        p = Program([If(IsNotSpace(), [Drop()], [MoveRight()]), LoopWhile(NotAtEnd(), [])])
        env = StringEnvironment("s t r i n g ", pos=0)

        env = p.interp(env)
        print(env.to_string())
        assert env.to_string() == "      "


class TestComplexPrograms(TestCase):

    def test_every_first_letter_uppercase(self):
        p = Program([
            If(AtStart(), [MakeUppercase()], []),
            Recurse(
                NotAtEnd(),
                [],
                [If(
                    IsSpace(),
                    [MoveRight(), MakeUppercase()],
                    [MoveRight()]
                )],
            )
        ])

        env = StringEnvironment("capitalize first letter of each word.")
        env = p.interp(env)
        assert env.to_string() == "Capitalize First Letter Of Each Word."