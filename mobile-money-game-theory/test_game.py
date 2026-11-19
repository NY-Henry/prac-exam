import unittest
from fractions import Fraction

from game import PRESETS, ProbabilityRange, analyze, parse_payoff


def preset(index):
    cells = list(PRESETS.values())[index]
    return (cells[:2], cells[2:])


class GameAnalysisTests(unittest.TestCase):
    def test_baseline_discount_dominates(self):
        result = analyze(preset(0))
        self.assertEqual(result.a_best, ((1,), (1,)))
        self.assertEqual(result.b_best, ((1,), (1,)))
        self.assertEqual(result.a_dominance, ((1, "strict"),))
        self.assertEqual(result.b_dominance, ((1, "strict"),))
        self.assertEqual(result.pure, ((1, 1),))
        self.assertEqual(result.mixed, ())

    def test_weaker_incentive_changes_equilibria(self):
        result = analyze(preset(1))
        self.assertEqual(result.pure, ((0, 0), (1, 1)))
        self.assertEqual(result.a_dominance, ())
        self.assertEqual(result.b_dominance, ())
        two_thirds = ProbabilityRange(Fraction(2, 3), Fraction(2, 3))
        self.assertEqual(result.mixed, ((two_thirds, two_thirds),))

    def test_matching_pennies_requires_mixing(self):
        result = analyze(preset(2))
        self.assertEqual(result.pure, ())
        half = ProbabilityRange(Fraction(1, 2), Fraction(1, 2))
        self.assertEqual(result.mixed, ((half, half),))

    def test_weak_dominance_and_partial_mixing(self):
        result = analyze((((1, 1), (1, 0)), ((1, 1), (0, 0))))
        self.assertEqual(result.a_dominance, ((0, "weak"),))
        self.assertEqual(result.a_best[0], (0, 1))
        self.assertEqual(result.pure, ((0, 0), (1, 0)))
        self.assertEqual(result.mixed, ((ProbabilityRange(0, 1, True, True), ProbabilityRange(1, 1)),))

    def test_all_ties_allow_every_probability_pair(self):
        result = analyze((((0, 0), (0, 0)), ((0, 0), (0, 0))))
        self.assertEqual(len(result.pure), 4)
        self.assertEqual(len(result.mixed), 5)
        self.assertEqual(result.a_dominance, ())
        self.assertIn((ProbabilityRange(0, 1, True, True),) * 2, result.mixed)

    def test_asymmetric_game_has_different_probabilities(self):
        result = analyze((((2, 3), (0, 0)), ((0, 0), (3, 2))))
        p, q = result.mixed[0]
        self.assertEqual((p.low, p.high, q.low, q.high), (Fraction(2, 5),) * 2 + (Fraction(3, 5),) * 2)

    def test_decimal_input_is_exact(self):
        self.assertEqual(parse_payoff(" -0.125 "), Fraction(-1, 8))
        self.assertEqual(parse_payoff("0.1") + parse_payoff("0.2"), parse_payoff("0.3"))

    def test_bad_inputs_are_rejected(self):
        for value in ("", "text", "NaN", "inf", "1/0", "1e100", "9" * 41):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_payoff(value)


if __name__ == "__main__":
    unittest.main()
