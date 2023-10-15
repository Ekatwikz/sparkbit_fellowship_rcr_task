# pylint: disable=protected-access
# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring

import unittest
from robotic_code_representation_generator \
    import RoboticCodeRepresentationGenerator as RCRG


class TestRoboticCodeRepresentationGenerator(unittest.TestCase):
    def test_blank_log_creates_no_codes(self):
        rcr_gen = RCRG([])
        self.assertEqual(rcr_gen._command_rcr_codes, {})

        with self.assertRaises(KeyError):
            rcr_gen.get_rcr("")
        with self.assertRaises(KeyError):
            rcr_gen.get_rcr("A")

    def test_single_node(self):
        rcr_gen = RCRG(["A", "A"])
        self.assertEqual(rcr_gen._command_rcr_codes, {"A": ""})

        self.assertEqual(rcr_gen.get_rcr("A"), "")
        with self.assertRaises(KeyError):
            rcr_gen.get_rcr("B")

    def test_state_initialized_properly(self):
        rcr_gen = RCRG(["A"])
        self.assertEqual(rcr_gen._command_rcr_codes, {"A": ""})
        self.assertEqual(rcr_gen.get_rcr("A"), "")
        rcr_gen = RCRG(["B", "B"])
        self.assertEqual(rcr_gen._command_rcr_codes, {"B": ""})
        self.assertEqual(rcr_gen.get_rcr("B"), "")
        with self.assertRaises(KeyError):
            rcr_gen.get_rcr("A")

    def test_two_nodes(self):
        rcr_gen = RCRG("B B A".split())
        self.assertEqual(len(rcr_gen._command_rcr_codes), 2)

        self.assertEqual(rcr_gen.get_rcr("A"), "0")
        self.assertEqual(rcr_gen.get_rcr("B"), "1")

    def test_medium_size_tree(self):
        rcr_gen = RCRG("".join([
            (i + " ") * j for (i, j) in
            zip("A B C D E F".split(), [1, 2, 4, 5, 10, 13])
            ]).split())
        self.assertEqual(len(rcr_gen._command_rcr_codes), 6)

        self.assertEqual(rcr_gen.get_rcr("A"), "11100")
        self.assertEqual(rcr_gen.get_rcr("B"), "11101")
        self.assertEqual(rcr_gen.get_rcr("C"), "1111")
        self.assertEqual(rcr_gen.get_rcr("D"), "110")
        self.assertEqual(rcr_gen.get_rcr("E"), "10")
        self.assertEqual(rcr_gen.get_rcr("F"), "0")

    def test_given_example(self):
        rcr_gen = RCRG("LEFT GRAB LEFT BACK LEFT BACK LEFT".split())
        self.assertEqual(len(rcr_gen._command_rcr_codes), 3)

        self.assertEqual(rcr_gen.get_rcr("GRAB"), "00")
        self.assertEqual(rcr_gen.get_rcr("BACK"), "01")
        self.assertEqual(rcr_gen.get_rcr("LEFT"), "1")


if __name__ == "__main__":
    unittest.main()
