# Ranks all submitted bids in descending order from highest to lowest.

BID_ENTRIES = [("Amina", 500), ("Brian", 650), ("Collins", 650), ("Doreen", 420)]


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


bids = load_bids(BID_ENTRIES)
print("Sorted:", rank_bids(bids))
