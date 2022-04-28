from unittest import TestCase

from common.program import Program
from common.tokens.pixel_tokens import *


class TestPixelTokens(TestCase):
    def setUp(self):
        self.env1 = PixelEnvironment(1, 1, 0, 0, [False])
        self.env2 = PixelEnvironment(3, 2, 0, 0)

    def test_draw(self):
        # print(Program([Draw()]).interp(self.env1).pixels)
        self.assertEqual(Program([Draw()]).interp(self.env1).pixels, (True,))
        self.assertEqual(Program([Draw(), Draw()]).interp(self.env1).pixels, (True,))

    def test_move(self):
        p1 = Program([MoveRight(), MoveRight(), MoveDown()])
        self.assertEqual(p1.interp(self.env2).pixels, (False, False, False, False, False, False))

    def test_move_exception(self):
        self.assertRaises(Exception, lambda: Program([MoveRight()]).interp(self.env1))
        self.assertRaises(Exception, lambda: Program([MoveLeft()]).interp(self.env1))
        self.assertRaises(Exception, lambda: Program([MoveUp()]).interp(self.env1))
        self.assertRaises(Exception, lambda: Program([MoveDown()]).interp(self.env1))

    def test_at(self):
        env1 = PixelEnvironment(3, 2, 0, 0)
        self.assertEqual(Program([AtTop()]).interp(env1), True)
        self.assertEqual(Program([AtLeft()]).interp(env1), True)
        env2 = PixelEnvironment(3, 2, 2, 1)
        self.assertEqual(Program([AtRight()]).interp(env2), True)
        self.assertEqual(Program([AtBottom()]).interp(env2), True)

    def test_draw_multiple(self):
        p1 = Program([MoveRight(), Draw(), MoveRight(), MoveDown(), Draw()])
        result = p1.interp(self.env2)
        expected = (False, True, False, False, False, True)
        self.assertEqual(expected, result.pixels)


class TestPixelDistance(TestCase):
    def test_pixel_distance(self):
        env1 = PixelEnvironment(2, 3, 0, 0, (False, True, False, True, False, False))
        env2 = PixelEnvironment(2, 3, 1, 2, (False, True, False, True, False, False))
        env3 = PixelEnvironment(2, 3, 1, 2, (False, False, False, True, True, False))
        self.assertEqual(0, env1.distance(env2))
        self.assertEqual(2, env1.distance(env3))

class TestPixelEquality(TestCase):
    def test_pixel_equality(self):
        env = PixelEnvironment(2, 3, 0, 0, (False, True, False, True, False, False))
        env_equal = PixelEnvironment(2, 3, 0, 0, (False, True, False, True, False, False))
        env_different = PixelEnvironment(2, 3, 0, 0, (False, False, False, True, False, False))
        self.assertEqual(env, env_equal)
        self.assertNotEqual(env, env_different)
        self.assertNotEqual(env_equal, env_different)