# Computes the auction winner and clearing price under first-price, second-price, or English rules.

BID_ENTRIES = [("Amina", 500), ("Brian", 650), ("Collins", 650), ("Doreen", 420)]
RESERVE_PRICE = 0
RULES_TO_SHOW = ["first-price", "second-price"]


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


bids = load_bids(BID_ENTRIES)
print("Sorted:", rank_bids(bids))
for auction_rule in RULES_TO_SHOW:
    print(auction_rule, settle_auction(bids, auction_rule, RESERVE_PRICE))
