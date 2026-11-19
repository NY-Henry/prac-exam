# Runs game simulation, auction settlement, and stable matching, then exports outcomes to JSON and CSV.

from collections import deque
import csv
import json
import random

PLAYER_NAMES = ["P1", "P2"]
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

BID_ENTRIES = [("Amina", 500), ("Brian", 650), ("Collins", 650), ("Doreen", 420)]
RESERVE_PRICE = 0
AUCTION_RULE_FOR_CSV = "second-price"

PROPOSER_PREFS = {
    "Alice": ["Makerere", "Ndejje", "Kyambogo"],
    "Bob": ["Ndejje", "Makerere", "Kyambogo"],
    "Cathy": ["Makerere", "Kyambogo", "Ndejje"],
}
RECEIVER_PREFS = {
    "Makerere": ["Bob", "Alice", "Cathy"],
    "Ndejje": ["Alice", "Bob", "Cathy"],
    "Kyambogo": ["Cathy", "Alice", "Bob"],
}

JSON_FILE = "game_results.json"
AUCTION_CSV_FILE = "auction_results.csv"
MATCHING_CSV_FILE = "matching_results.csv"


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


def is_pure_nash(table, row_idx, col_idx):
    p1_payoff = table[row_idx][col_idx][0]
    p2_payoff = table[row_idx][col_idx][1]
    best_for_p1 = all(p1_payoff >= table[r][col_idx][0] for r in range(len(table)))
    best_for_p2 = all(p2_payoff >= table[row_idx][c][1] for c in range(len(table[0])))
    return best_for_p1 and best_for_p2


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


def export_json(filepath, game_data, result_data):
    with open(filepath, "w", encoding="utf-8") as handle:
        json.dump({"game": game_data, "outcomes": result_data}, handle, indent=2)
    print("Saved to", filepath)


def deferred_acceptance(proposer_prefs, receiver_prefs):
    unmatched = deque(proposer_prefs.keys())
    cursor = {p: 0 for p in proposer_prefs}
    rank_lookup = {
        rec: {prop: idx for idx, prop in enumerate(pref_list)}
        for rec, pref_list in receiver_prefs.items()
    }
    assignments = {}
    while unmatched:
        prop = unmatched.popleft()
        if cursor[prop] >= len(proposer_prefs[prop]):
            continue
        rec = proposer_prefs[prop][cursor[prop]]
        cursor[prop] += 1
        if prop not in rank_lookup.get(rec, {}):
            unmatched.append(prop)
        elif rec not in assignments:
            assignments[rec] = prop
        else:
            current = assignments[rec]
            if rank_lookup[rec][prop] < rank_lookup[rec][current]:
                unmatched.append(current)
                assignments[rec] = prop
            else:
                unmatched.append(prop)
    return assignments


def load_bids(entries=None):
    if entries is not None:
        return dict(entries)
    bid_map = {}
    count = int(input("Number of bidders: "))
    for _ in range(count):
        bidder = input("Name: ").strip()
        while True:
            raw = input(f"Bid for {bidder}: ")
            try:
                value = float(raw)
                if value >= 0:
                    bid_map[bidder] = value
                    break
            except ValueError:
                pass
            print("Please enter a non-negative number.")
    return bid_map


def rank_bids(bid_map):
    return sorted(bid_map.items(), key=lambda pair: pair[1], reverse=True)


def settle_auction(bid_map, rule="first-price", reserve=0):
    ordered = rank_bids(bid_map)
    winner, top_bid = ordered[0]
    if top_bid < reserve:
        return None, 0
    if rule == "first-price":
        clearing_price = top_bid
    elif rule in ("second-price", "english"):
        runner_up = ordered[1][1] if len(ordered) > 1 else 0
        clearing_price = max(runner_up, reserve)
    else:
        raise ValueError("Unknown rule")
    return winner, clearing_price


def export_csv(filepath, columns, rows):
    with open(filepath, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)
    print("Saved", filepath)


game_log, total_scores = run_repeated_game(
    NUM_ROUNDS,
    STRATEGIES[P1_STRATEGY_NAME],
    STRATEGIES[P2_STRATEGY_NAME],
    PAYOFF_TABLE,
    RANDOM_SEED,
)
equilibria = [
    (ROW_ACTIONS[r], COL_ACTIONS[c])
    for r in range(len(ROW_ACTIONS))
    for c in range(len(COL_ACTIONS))
    if is_pure_nash(PAYOFF_TABLE, r, c)
]
export_json(
    JSON_FILE,
    {"players": PLAYER_NAMES, "strategies": [ROW_ACTIONS, COL_ACTIONS], "payoffs": PAYOFF_TABLE},
    {"nash_equilibria": equilibria, "repeated_game_totals": total_scores},
)

result_matching = deferred_acceptance(PROPOSER_PREFS, RECEIVER_PREFS)
bids = load_bids(BID_ENTRIES)
print("Sorted:", rank_bids(bids))
for mech in ["first-price", "second-price"]:
    print(mech, settle_auction(bids, mech, RESERVE_PRICE))

winner_name, clearing_price = settle_auction(bids, AUCTION_RULE_FOR_CSV, RESERVE_PRICE)
auction_rows = [
    [bidder, amount, bidder == winner_name, clearing_price if bidder == winner_name else 0]
    for bidder, amount in rank_bids(bids)
]
export_csv(AUCTION_CSV_FILE, ["bidder", "bid", "winner", "price_paid"], auction_rows)
export_csv(MATCHING_CSV_FILE, ["university", "student"], sorted(result_matching.items()))
