# Builds and prints a two-player normal-form payoff table.

ROW_ACTIONS = ["Cooperate", "Defect"]
COL_ACTIONS = ["Cooperate", "Defect"]
PAYOFF_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)],
]
COL_WIDTH = 12


def render_payoff_table(table, row_labels, col_labels, width=12):
    top_row = "P1 \\ P2".ljust(width) + "".join(label.rjust(width) for label in col_labels)
    print(top_row)
    for r_idx, r_name in enumerate(row_labels):
        cells = "".join(str(table[r_idx][c_idx]).rjust(width) for c_idx in range(len(col_labels)))
        print(r_name.ljust(width) + cells)


render_payoff_table(PAYOFF_TABLE, ROW_ACTIONS, COL_ACTIONS, COL_WIDTH)
