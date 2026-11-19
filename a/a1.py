# Stores and prints the available action names for Player 1 and Player 2.

P1_ACTIONS = ["Cooperate", "Defect"]
P2_ACTIONS = ["Cooperate", "Defect"]


def show_actions(label, actions):
    print(f"{label}: {actions}")


show_actions("Player 1 strategies", P1_ACTIONS)
show_actions("Player 2 strategies", P2_ACTIONS)

# File Guide (prac exam):
# a/a1.py  - Store and print P1 and P2 action lists
# a/a2.py  - Build and print a 2-player payoff matrix table
# a/a3.py  - Find best-response actions and payoff for a fixed opponent move
# a/a4.py  - Check if either player has a dominant strategy
# a/a5.py  - Find all pure-strategy Nash equilibria in the payoff matrix
# a/a6.py  - Compute expected payoffs for mixed strategy probability vectors
# a/a7.py  - Simulate a repeated game round-by-round and total the payoffs
# a/a8.py  - Calculate discounted present value (delta) of a reward stream
# a/a9.py  - Compare two repeated-game strategies vs an opponent (sum & PV)
# a/a10.py - Find Nash equilibria, simulate repeated game, and export JSON
# b/b1.py  - Collect bidder names and non-negative bids into a dictionary
# b/b2.py  - Sort submitted bids from highest to lowest
# b/b3.py  - Pick auction winner and resolve ties ('first' or 'random')
# b/b4.py  - Compute winner and clearing price (first-price, second-price, english)
# b/b5.py  - Calculate bidder quasi-linear utility (valuation - price paid)
# b/b6.py  - Compare seller revenue and winners across auction mechanisms
# b/b7.py  - Store and print preference lists for a two-sided matching market
# b/b8.py  - Run Gale-Shapley deferred acceptance for a stable matching
# b/b9.py  - Check if a matching is stable or has blocking pairs
# b/b10.py - Run game, auction, and matching workflows and export JSON/CSV


