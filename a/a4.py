# Finds whether either player has a dominant strategy across all opponent choices.

ROW_ACTIONS = ["Cooperate", "Defect"]
COL_ACTIONS = ["Cooperate", "Defect"]
PAYOFF_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)],
]


def find_dominant_action(table, player_idx):
    num_rows = len(table)
    num_cols = len(table[0])
    if player_idx == 0:
        for r in range(num_rows):
            if all(table[r][c][0] >= table[alt][c][0] for alt in range(num_rows) if alt != r for c in range(num_cols)):
                return r
    else:
        for c in range(num_cols):
            if all(table[r][c][1] >= table[r][alt][1] for alt in range(num_cols) if alt != c for r in range(num_rows)):
                return c
    return None


dom_p1 = find_dominant_action(PAYOFF_TABLE, 0)
dom_p2 = find_dominant_action(PAYOFF_TABLE, 1)
print("P1 dominant:", ROW_ACTIONS[dom_p1] if dom_p1 is not None else "none")
print("P2 dominant:", COL_ACTIONS[dom_p2] if dom_p2 is not None else "none")
