import unittest

from common_environment.control_tokens import *
from common_environment.environment import *
from interpreter.interpreter import Program
from string_environment.string_tokens import *


class TestTokens(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(MoveRight(), MoveRight())
        self.assertNotEqual(MoveLeft(), MoveRight())
        self.assertEqual(InventedToken([MoveLeft(), MoveRight()]), InventedToken([MoveLeft(), MoveRight()]))
        self.assertNotEqual(InventedToken([MoveRight(), MoveLeft()]), InventedToken([MoveLeft(), MoveRight()]))
        self.assertNotEqual(InventedToken([MoveLeft()]), InventedToken([MoveLeft(), MoveRight()]))
