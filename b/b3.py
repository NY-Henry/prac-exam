# Determines the auction winner and resolves ties using a configurable tie-breaking rule.

import random

BID_ENTRIES = [("Amina", 500), ("Brian", 650), ("Collins", 650), ("Doreen", 420)]
TIE_RULE = "first"
RANDOM_SEED = 1


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


def resolve_winner(bid_map, tie_rule="first", seed=1):
    max_bid = max(bid_map.values())
    contenders = [name for name, amount in bid_map.items() if amount == max_bid]
    if len(contenders) > 1:
        print(f"Tie between {contenders} at {max_bid}")
    if tie_rule == "first":
        chosen = contenders[0]
    elif tie_rule == "random":
        random.seed(seed)
        chosen = random.choice(contenders)
    else:
        raise ValueError("Unsupported tie rule")
    return chosen, max_bid


bids = load_bids(BID_ENTRIES)
print("Winner:", resolve_winner(bids, TIE_RULE, RANDOM_SEED))
