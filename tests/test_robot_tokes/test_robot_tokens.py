from unittest import TestCase

from common.program import Program
from common.tokens.robot_tokens import *


class TestRobotTokens(TestCase):
    def setUp(self):
        self.env1 = RobotEnvironment(1, 0, 0, 0, 0, False)
        self.env2 = RobotEnvironment(1, 0, 0, 0, 0, True)
        self.env3 = RobotEnvironment(3, 1, 0, 1, 1, False)

    def test_at(self):
        env1 = RobotEnvironment(3, 0, 0, 2, 2, False)
        self.assertTrue(Program([AtTop()]).interp(env1))
        self.assertTrue(Program([AtLeft()]).interp(env1))
        self.assertFalse(Program([AtRight()]).interp(env1))
        self.assertFalse(Program([AtBottom()]).interp(env1))
        env2 = RobotEnvironment(3, 2, 2, 0, 0, False)
        self.assertFalse(Program([AtTop()]).interp(env2))
        self.assertFalse(Program([AtLeft()]).interp(env2))
        self.assertTrue(Program([AtRight()]).interp(env2))
        self.assertTrue(Program([AtBottom()]).interp(env2))
        env3 = RobotEnvironment(4, 3, 1, 0, 0, False)
        self.assertTrue(Program([AtRight()]).interp(env3))
        self.assertFalse(Program([AtLeft()]).interp(env3))

    def test_move(self):
        p1 = Program([MoveRight(), MoveDown(), MoveDown()])
        res = p1.interp(self.env3)
        self.assertEqual(res.rx, 2)
        self.assertEqual(res.ry, 2)

    def test_move_exception(self):
        self.assertRaises(Exception, lambda: Program([MoveRight()]).interp(self.env1))
        self.assertRaises(Exception, lambda: Program([MoveLeft()]).interp(self.env1))
        self.assertRaises(Exception, lambda: Program([MoveUp()]).interp(self.env1))
        self.assertRaises(Exception, lambda: Program([MoveDown()]).interp(self.env1))
        self.assertRaises(Exception, lambda: Program([MoveRight(), MoveRight()]).interp(self.env3))

    def test_grab(self):
        self.assertFalse(self.env1.holding)
        self.assertTrue(Program([Grab()]).interp(self.env1).holding)

    def test_double_grab(self):
        self.assertFalse(self.env1.holding)
        self.assertRaises(Exception, lambda: Program([Grab(), Grab()]).interp(self.env1))

    def test_grab_miss(self):
        self.assertRaises(Exception, lambda: Program([Grab()]).interp(self.env3))

    def test_drop(self):
        self.assertFalse(Program([Drop()]).interp(self.env2).holding)

    def test_double_drop(self):
        self.assertRaises(Exception, lambda: Program([Drop(), Drop()]).interp(self.env2))


class TestRobotDistance(TestCase):
    def test_robot_distance(self):
        env1 = RobotEnvironment(2, 0, 0, 1, 0, False)
        env2 = RobotEnvironment(2, 1, 1, 1, 1, True)
        self.assertEqual(4, env1.distance(env2))
