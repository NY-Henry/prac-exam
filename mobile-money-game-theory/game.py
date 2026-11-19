"""Exact best responses, dominance and Nash equilibria for two-player 2×2 games."""

import re
from dataclasses import dataclass
from fractions import Fraction

Payoff = tuple[Fraction, Fraction]
Matrix = tuple[tuple[Payoff, Payoff], tuple[Payoff, Payoff]]
SUPPORTS = ((0,), (1,), (0, 1))
ACTIONS = ("Standard", "Discounted")
PRESETS = {
    "Baseline · strong discount incentive": ((8, 8), (2, 10), (10, 2), (4, 4)),
    "Scenario · weaker discount incentive": ((8, 8), (2, 7), (7, 2), (4, 4)),
    "Validation · Matching Pennies": ((1, -1), (-1, 1), (-1, 1), (1, -1)),
}


def parse_payoff(raw: str) -> Fraction:
    value = raw.strip()
    if len(value) > 40 or not re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)", value):
        raise ValueError("Enter an integer or decimal, such as 8, -2 or 3.5.")
    return Fraction(value)


@dataclass(frozen=True)
class ProbabilityRange:
    low: Fraction
    high: Fraction
    open_low: bool = False
    open_high: bool = False

    def __str__(self) -> str:
        if self.low == self.high:
            return str(self.low)
        left = "(" if self.open_low else "["
        right = ")" if self.open_high else "]"
        return f"{left}{self.low}, {self.high}{right}"


@dataclass(frozen=True)
class Analysis:
    a_best: tuple[tuple[int, ...], ...]
    b_best: tuple[tuple[int, ...], ...]
    a_dominance: tuple[tuple[int, str], ...]
    b_dominance: tuple[tuple[int, str], ...]
    pure: tuple[tuple[int, int], ...]
    mixed: tuple[tuple[ProbabilityRange, ProbabilityRange], ...]


def best_actions(difference: Fraction) -> tuple[int, ...]:
    if difference > 0:
        return (0,)
    if difference < 0:
        return (1,)
    return (0, 1)


def dominance(differences: tuple[Fraction, Fraction]) -> tuple[tuple[int, str], ...]:
    for action, sign in ((0, 1), (1, -1)):
        margins = tuple(sign * difference for difference in differences)
        if min(margins) > 0:
            return ((action, "strict"),)
        if min(margins) == 0 and max(margins) > 0:
            return ((action, "weak"),)
    return ()


def allowed_probability(
    own_support: tuple[int, ...],
    other_support: tuple[int, ...],
    difference_at_zero: Fraction,
    difference_at_one: Fraction,
) -> ProbabilityRange | None:
    """Restrict own first-action probability to make the other support optimal."""
    low = Fraction(1 if own_support == (0,) else 0)
    high = Fraction(0 if own_support == (1,) else 1)
    constant = difference_at_zero
    slope = difference_at_one - difference_at_zero

    if other_support == (0, 1):
        if slope == 0:
            if constant != 0:
                return None
        else:
            root = -constant / slope
            low, high = max(low, root), min(high, root)
    else:
        # Require first payoff minus second payoff >= 0, or reverse for action 2.
        if other_support == (1,):
            constant, slope = -constant, -slope
        if slope > 0:
            low = max(low, -constant / slope)
        elif slope < 0:
            high = min(high, -constant / slope)
        elif constant < 0:
            return None

    open_low = own_support == (0, 1) and low == 0
    open_high = own_support == (0, 1) and high == 1
    if low > high or (low == high and (open_low or open_high)):
        return None
    return ProbabilityRange(low, high, open_low, open_high)


def analyze(matrix: Matrix) -> Analysis:
    a_differences = tuple(Fraction(matrix[0][col][0] - matrix[1][col][0]) for col in range(2))
    b_differences = tuple(Fraction(matrix[row][0][1] - matrix[row][1][1]) for row in range(2))
    a_best = tuple(best_actions(difference) for difference in a_differences)
    b_best = tuple(best_actions(difference) for difference in b_differences)
    pure = tuple((row, col) for row in range(2) for col in range(2)
                 if row in a_best[col] and col in b_best[row])

    mixed = []
    for a_support in SUPPORTS:
        for b_support in SUPPORTS:
            if len(a_support) == len(b_support) == 1:
                continue
            p = allowed_probability(a_support, b_support, b_differences[1], b_differences[0])
            q = allowed_probability(b_support, a_support, a_differences[1], a_differences[0])
            if p is not None and q is not None:
                mixed.append((p, q))
    return Analysis(a_best, b_best, dominance(a_differences), dominance(b_differences), pure, tuple(mixed))
