# Checks every strategy pair to find all pure-strategy Nash equilibria.

ROW_ACTIONS = ["Cooperate", "Defect"]
COL_ACTIONS = ["Cooperate", "Defect"]
PAYOFF_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)],
]


def is_pure_nash(table, row_idx, col_idx):
    p1_payoff = table[row_idx][col_idx][0]
    p2_payoff = table[row_idx][col_idx][1]
    best_for_p1 = all(p1_payoff >= table[r][col_idx][0] for r in range(len(table)))
    best_for_p2 = all(p2_payoff >= table[row_idx][c][1] for c in range(len(table[0])))
    return best_for_p1 and best_for_p2


for r_idx, r_name in enumerate(ROW_ACTIONS):
    for c_idx, c_name in enumerate(COL_ACTIONS):
        status = "(*Nash)" if is_pure_nash(PAYOFF_TABLE, r_idx, c_idx) else "-"
        print(r_name, c_name, status)
