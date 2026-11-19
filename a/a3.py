# Computes a player's best-response actions and maximum payoff when the opponent's move is fixed.

ROW_ACTIONS = ["Cooperate", "Defect"]
COL_ACTIONS = ["Cooperate", "Defect"]
PAYOFF_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)],
]


def best_reply_p1(table, col_idx):
    scores = [table[r_idx][col_idx][0] for r_idx in range(len(table))]
    peak = max(scores)
    chosen = [r_idx for r_idx, val in enumerate(scores) if val == peak]
    return peak, chosen


def best_reply_p2(table, row_idx):
    scores = [table[row_idx][c_idx][1] for c_idx in range(len(table[0]))]
    peak = max(scores)
    chosen = [c_idx for c_idx, val in enumerate(scores) if val == peak]
    return peak, chosen


for c_idx, opp_name in enumerate(COL_ACTIONS):
    peak_val, best_rows = best_reply_p1(PAYOFF_TABLE, c_idx)
    names = [ROW_ACTIONS[r_idx] for r_idx in best_rows]
    print(f"If P2 plays {opp_name}, P1's best payoff is {peak_val} using {names}")
