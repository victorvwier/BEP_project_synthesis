from unittest import TestCase

from common_environment.environment import StringEnvironment


class TestRobotEnvironment(TestCase):
    pass

class TestStringEnvironment(TestCase):
    def test_to_string(self):
        s1 = "Hello World"
        e1 = StringEnvironment(s1)
        self.assertEqual(e1.toString(), s1)

        s2 = "String!"
        e1 = StringEnvironment(s2)
        self.assertEqual(e1.toString(), s2)

    def _dist(self, a, b):
        a1 = StringEnvironment(a)
        b1 = StringEnvironment(b)
        return a1.distance(b1)

    def test_distance(self):
        a1 = "Hello world"
        a2 = "Hello World!"
        self.assertEqual(self._dist(a1, a2), 2)

        a1 = "Hello world"
        a2 = "Hello world"
        self.assertEqual(self._dist(a1, a2), 0)

        a1 = "Hello world"
        a2 = "H1elo, worllD"
        self.assertEqual(self._dist(a1, a2), 5)

    def test_correct(self):
        a1 = "Hello world"
        a2 = "Hello world"
        e1 = StringEnvironment(a1, pos=0)
        e2 = StringEnvironment(a2, pos=3)

        self.assertTrue(e1.correct(e2))