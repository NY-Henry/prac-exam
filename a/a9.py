# Compares two repeated-game strategies against a chosen opponent using total and discounted payoffs.

import random

ROW_ACTIONS = ["Cooperate", "Defect"]
COL_ACTIONS = ["Cooperate", "Defect"]
PAYOFF_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)],
]
NUM_ROUNDS = 10
DISCOUNT_FACTOR = 0.9
RANDOM_SEED = 1
CANDIDATE_A = "grim_trigger"
CANDIDATE_B = "always_defect"
OPPONENT = "tit_for_tat"


def always_cooperate(history):
    return 0


def always_defect(history):
    return 1


def tit_for_tat(history):
    return 0 if not history else history[-1][1]


def tit_for_two_tats(history):
    if len(history) >= 2 and history[-1][1] == 1 and history[-2][1] == 1:
        return 1
    return 0


def grim_trigger(history):
    return 1 if any(opp_move == 1 for _, opp_move in history) else 0


def random_move(history):
    return random.choice([0, 1])


STRATEGIES = {
    "always_cooperate": always_cooperate,
    "always_defect": always_defect,
    "tit_for_tat": tit_for_tat,
    "tit_for_two_tats": tit_for_two_tats,
    "grim_trigger": grim_trigger,
    "random_move": random_move,
}


def discounted_total(rewards, delta):
    total = 0.0
    factor = 1.0
    for reward in rewards:
        total += reward * factor
        factor *= delta
    return total


def benchmark_against_opponent(names, opponent_name, table, rounds=10, delta=0.9, seed=1):
    opp_fn = STRATEGIES[opponent_name]
    summary = {}
    for name in names:
        random.seed(seed)
        fn = STRATEGIES[name]
        pairs = []
        rewards = []
        for _ in range(rounds):
            p1_view = [(a, b) for a, b in pairs]
            p2_view = [(b, a) for a, b in pairs]
            m1 = fn(p1_view)
            m2 = opp_fn(p2_view)
            rewards.append(table[m1][m2][0])
            pairs.append((m1, m2))
        summary[name] = (sum(rewards), round(discounted_total(rewards, delta), 2))
    return summary


outcome = benchmark_against_opponent(
    [CANDIDATE_A, CANDIDATE_B],
    OPPONENT,
    PAYOFF_TABLE,
    NUM_ROUNDS,
    DISCOUNT_FACTOR,
    RANDOM_SEED,
)
print(f"vs {OPPONENT}:", outcome)
