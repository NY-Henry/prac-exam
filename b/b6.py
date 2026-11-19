# Compares seller revenue and winners across first-price, second-price, and English auction mechanisms.

BID_ENTRIES = [("Amina", 500), ("Brian", 650), ("Collins", 650), ("Doreen", 420)]
RESERVE_PRICE = 0
MECHANISMS = ["first-price", "second-price", "english"]


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


def show_revenue_table(bid_map, mechanisms, reserve=0):
    print("Mechanism".ljust(15) + "Winner".ljust(10) + "Revenue".rjust(10))
    for mech in mechanisms:
        winner, revenue = settle_auction(bid_map, mech, reserve)
        print(mech.ljust(15) + str(winner).ljust(10) + str(revenue).rjust(10))


bids = load_bids(BID_ENTRIES)
print("Sorted:", rank_bids(bids))
for mech in ["first-price", "second-price"]:
    print(mech, settle_auction(bids, mech, RESERVE_PRICE))
show_revenue_table(bids, MECHANISMS, RESERVE_PRICE)
