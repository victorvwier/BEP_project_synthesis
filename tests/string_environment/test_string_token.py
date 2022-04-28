from unittest import TestCase

from common.tokens.control_tokens import *
from common.program import Program
from common.tokens.string_tokens import *
from common.environment import StringEnvironment


class TestStringTransTokens(TestCase):
    def test_move_right(self):
        p1 = Program([MoveRight()])
        env = StringEnvironment(["s", "t", "r", "i", "n", "g"])

        env = p1.interp(env)
        self.assertEqual(env.pos, 1)

        env = p1.interp(env)
        self.assertEqual(env.pos, 2)

        p2 = Program([MoveRight(), MoveRight(), MoveRight()])
        env = p2.interp(env)
        self.assertEqual(env.pos, 5)

        self.assertRaises(InvalidTransition, lambda : p1.interp(env))

    def test_move_left(self):
        p1 = Program([MoveLeft()])
        env = StringEnvironment(["s", "t", "r", "i", "n", "g"], pos = 5)

        env = p1.interp(env)
        self.assertEqual(env.pos, 4)

        env = p1.interp(env)
        self.assertEqual(env.pos, 3)

        p2 = Program([MoveLeft(), MoveLeft(), MoveLeft()])
        env = p2.interp(env)
        self.assertEqual(env.pos, 0)

        self.assertRaises(InvalidTransition, lambda : p1.interp(env))

    def test_make_uppercase(self):
        p1 = Program([MakeUppercase(), MoveRight(), MoveRight(), MakeUppercase(), MoveRight(), MakeUppercase()])
        env = StringEnvironment(["s", "t", "r", "i", "n", "g"])

        env = p1.interp(env)
        self.assertEqual(env.string_array, list("StRIng"))

    def test_make_lowercase(self):
        p1 = Program([MakeLowercase(), MoveLeft(), MoveLeft(), MakeLowercase(), MoveLeft(), MakeLowercase()])
        env = StringEnvironment(list("STRING"), pos = 5)

        env = p1.interp(env)
        self.assertEqual(env.string_array, list("STriNg"))

    def test_drop(self):
        p1 = Program([MoveLeft(), Drop()])
        p2 = Program([MoveLeft(), Drop(), Drop()])
        env = StringEnvironment(list("string"), pos=5)

        env = p1.interp(env)
        self.assertEqual(env.string_array, list("strig"))
        self.assertEqual(env.pos, 4)

        env = p2.interp(env)
        self.assertEqual(env.string_array, list("str"))
        self.assertEqual(env.pos, 2)

    def test_drop_all(self):
        p1 = Program([Drop()])
        ei = StringEnvironment(["s"])
        eo = StringEnvironment([""])

        ei = p1.interp(ei)
        self.assertTrue(ei.correct(eo))

    def test_drop_empty(self):
        p = Program([Drop()])
        env = StringEnvironment(list(""))

        self.assertRaises(InvalidTransition, lambda : p.interp(env))


class TestStringBoolTokens(TestCase):

    def test_at_end(self):
        p = Program([If(AtEnd(), [], [MoveRight()]), If(AtEnd(), [], [MoveRight()]), If(AtEnd(), [], [MoveRight()])])
        env = StringEnvironment(list("str"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.pos, 2)

    def test_not_at_end(self):
        p = Program([LoopWhile(NotAtEnd(), [MoveRight()])])
        env = StringEnvironment(list("str"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.pos, 2)

    def test_at_start(self):
        p = Program([If(AtStart(), [], [MoveLeft()]), If(AtStart(), [], [MoveLeft()]), If(AtStart(), [], [MoveLeft()])])
        env = StringEnvironment(list("str"), pos=2)

        env = p.interp(env)
        self.assertEqual(env.pos, 0)

    def test_not_at_start(self):
        p = Program([LoopWhile(NotAtStart(),[MoveLeft()])])
        env = StringEnvironment(list("str"), pos=2)

        env = p.interp(env)
        self.assertEqual(env.pos, 0)

    def test_is_letter(self):
        p = Program([LoopWhile(NotAtEnd(), [If(IsLetter(), [Drop()], [MoveRight()])]), If(IsLetter(), [Drop()], [])])
        env = StringEnvironment(list("s1t2se3CK4cko5"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.to_string(), "12345")

    def test_is_not_letter(self):
        p = Program([LoopWhile(NotAtEnd(), [If(IsNotLetter(), [Drop()], [MoveRight()])]), If(IsNotLetter(), [Drop()], [])])
        env = StringEnvironment(list("12s3t9ri398n5092g"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.to_string(), "string")

    def test_is_uppercase(self):
        p = Program([LoopWhile(NotAtEnd(), [If(IsUppercase(), [MoveRight()], [Drop()])]), If(IsUppercase(), [], [Drop()])])
        env = StringEnvironment(list("diSjdTjidRiqINjqG"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.to_string(), "STRING")

    def test_is_not_uppercase(self):
        p = Program([LoopWhile(NotAtEnd(), [If(IsNotUppercase(), [Drop()], [MoveRight()])]), If(IsNotUppercase(), [Drop()], [])])
        env = StringEnvironment(list("d489iSjdTjidRi13qINjqG"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.to_string(), "STRING")

    def test_is_lowercase(self):
        p = Program([LoopWhile(NotAtEnd(), [If(IsLowercase(), [MoveRight()], [Drop()])]), If(IsLowercase(), [], [Drop()])])
        env = StringEnvironment(list("12sRGM4tr34iNOKFn34g"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.to_string(), "string")

    def test_is_not_lowercase(self):
        p = Program([LoopWhile(NotAtEnd(), [If(IsNotLowercase(), [Drop()], [MoveRight()])]), If(IsNotLowercase(), [Drop()], [])])
        env = StringEnvironment(list("12sRGM4tr34iNOKFn34g"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.to_string(), "string")

    def test_is_number(self):
        p = Program([LoopWhile(NotAtEnd(), [If(IsNumber(), [Drop()], [MoveRight()])]), If(IsNumber(), [Drop()], [])])
        env = StringEnvironment(list("1234s50t049r"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.to_string(), "str")

    def test_is_not_number(self):
        p = Program([LoopWhile(NotAtEnd(), [If(IsNotNumber(), [Drop()], [MoveRight()])]), If(IsNotNumber(), [Drop()], [])])
        env = StringEnvironment(list("ha@1j2^&*3"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.to_string(), "123")

    def test_is_space(self):
        p = Program([LoopWhile(NotAtEnd(), [If(IsSpace(), [Drop()], [MoveRight()])]), If(IsSpace(), [Drop()], [])])
        env = StringEnvironment(list("s t r i n g"), pos=0)

        env = p.interp(env)
        self.assertEqual(env.to_string(), "string")

    def test_is_not_space(self):
        p = Program([LoopWhile(NotAtEnd(), [If(IsNotSpace(), [Drop()], [MoveRight()])]), If(IsNotSpace(), [Drop()], [])])
        env = StringEnvironment(list("s t r i n g "), pos=0)

        env = p.interp(env)
        print(env.to_string())
        self.assertEqual(env.to_string(), "      ")

    def test_infinite_negative_pos_bug(self):
        env = StringEnvironment(["a"])
        env = Program([Drop()]).interp(env)
        self.assertEqual(StringEnvironment([], pos=0), env)
        self.assertRaises(InvalidTransition, lambda: Program([MoveLeft()]).interp(env))

    def test_infinite_positive_pos_bug(self):
        env = StringEnvironment(["a"])
        env = Program([Drop()]).interp(env)
        self.assertEqual(StringEnvironment([], pos=0), env)
        self.assertRaises(InvalidTransition, lambda: Program([MoveRight()]).interp(env))

# class TestComplexPrograms(TestCase):

#     def test_every_first_letter_uppercase(self):
#         p = Program([
#             LoopWhile(NotAtEnd(), 
#                 [If(IsSpace(),
#                     [],
#                     [])]
#             )
#         ])

#         env = StringEnvironment("capitalize first letter of each word.")
#         env = p.interp(env)
#         assert env.to_string() == "Capitalize First Letter Of Each Word."