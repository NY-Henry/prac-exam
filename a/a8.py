# Computes the discounted present value of a sequence of per-round rewards.

REWARD_STREAM = [3, 3, 3, 3, 3]
DISCOUNT_FACTOR = 0.9
ROUND_DIGITS = 3


def discounted_total(rewards, delta):
    total = 0.0
    factor = 1.0
    for reward in rewards:
        total += reward * factor
        factor *= delta
    return total


pv = round(discounted_total(REWARD_STREAM, DISCOUNT_FACTOR), ROUND_DIGITS)
print(f"PV of {len(REWARD_STREAM)} rounds at delta={DISCOUNT_FACTOR}:", pv)
