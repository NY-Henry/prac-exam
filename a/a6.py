# Calculates expected payoffs for both players under mixed strategy probability vectors.

PAYOFF_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)],
]
P1_PROBS = [0.5, 0.5]
P2_PROBS = [0.3, 0.7]
TOLERANCE = 1e-9


def check_distribution(probs):
    if any(prob < 0 for prob in probs) or abs(sum(probs) - 1.0) > TOLERANCE:
        raise ValueError("Probabilities must be non-negative and sum to 1")


def mixed_expected_payoffs(table, p1_probs, p2_probs):
    check_distribution(p1_probs)
    check_distribution(p2_probs)
    exp_p1 = 0.0
    exp_p2 = 0.0
    for r_idx, pr_r in enumerate(p1_probs):
        for c_idx, pr_c in enumerate(p2_probs):
            weight = pr_r * pr_c
            exp_p1 += weight * table[r_idx][c_idx][0]
            exp_p2 += weight * table[r_idx][c_idx][1]
    return exp_p1, exp_p2


print("Expected payoffs:", mixed_expected_payoffs(PAYOFF_TABLE, P1_PROBS, P2_PROBS))
