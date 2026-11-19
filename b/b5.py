# Calculates a bidder's quasi-linear utility from their valuation and payment.

VALUATION = 700
PRICE_PAID = 650
IS_WINNER = True


def bidder_utility(valuation, payment_amount, won=True):
    return valuation - payment_amount if won else 0


print(
    f"Utility of valuation {VALUATION} paying {PRICE_PAID}:",
    bidder_utility(VALUATION, PRICE_PAID, IS_WINNER),
)
