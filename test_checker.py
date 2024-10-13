import unittest
import checker

class TestChecker(unittest.TestCase):
    # TODO !!!
    def test_white_cross_check(self):
        result = checker.white_cross_check({})
        self.assertFalse(result)

        result = checker.white_cross_check({})
        self.assertTrue(result)
        pass

    # TODO !!!
    def test_white_corners_check(self):
        pass

    # TODO !!!
    def test_middle_edge(self):
        pass

    # TODO !!!
    def test_yellow_pattern_switch(self):
        pass

    # TODO !!!
    def test_yellow_dot(self):
        pass

    # TODO !!!
    def test_yellow_L(self):
        pass

    # TODO !!!
    def test_yellow_line(self):
        pass

    # TODO !!!
    def test_yellow_cross(self):
        pass

    # TODO !!!
    def test_yellow_edge(self):
        pass

    # TODO !!!
    def test_yellow_corners(self):
        pass

    # TODO !!!
    def test_yellow_corners_solved(self):
        pass

if __name__ == '__main__':
    unittest.main()