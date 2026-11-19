# Simulates a repeated two-player game round by round and totals each player's score.

import random

ROW_ACTIONS = ["Cooperate", "Defect"]
COL_ACTIONS = ["Cooperate", "Defect"]
PAYOFF_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)],
]
NUM_ROUNDS = 5
RANDOM_SEED = 1
P1_STRATEGY_NAME = "tit_for_tat"
P2_STRATEGY_NAME = "random_move"


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


def run_repeated_game(rounds, fn1, fn2, table, seed=1):
    random.seed(seed)
    log = []
    scores = [0, 0]
    for step in range(1, rounds + 1):
        p1_view = [(entry[0], entry[1]) for entry in log]
        p2_view = [(entry[1], entry[0]) for entry in log]
        move1 = fn1(p1_view)
        move2 = fn2(p2_view)
        pay1, pay2 = table[move1][move2]
        scores[0] += pay1
        scores[1] += pay2
        log.append((move1, move2, pay1, pay2))
        print(f"Round {step}: P1={ROW_ACTIONS[move1]}, P2={COL_ACTIONS[move2]}, payoffs=({pay1},{pay2})")
    return log, scores


game_log, total_scores = run_repeated_game(
    NUM_ROUNDS,
    STRATEGIES[P1_STRATEGY_NAME],
    STRATEGIES[P2_STRATEGY_NAME],
    PAYOFF_TABLE,
    RANDOM_SEED,
)
print("Totals:", total_scores)
