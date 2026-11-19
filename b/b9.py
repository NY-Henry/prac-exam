# Verifies whether a two-sided matching is stable by detecting any blocking pairs.

from collections import deque

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
TEST_BAD_MATCHING = {"Makerere": "Cathy", "Ndejje": "Alice", "Kyambogo": "Bob"}


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


def ranks_higher(pref_table, agent, candidate, current_partner):
    ranking = pref_table[agent]
    if candidate not in ranking:
        return False
    if current_partner is None or current_partner not in ranking:
        return True
    return ranking.index(candidate) < ranking.index(current_partner)


def check_stability(assignments, proposer_prefs, receiver_prefs):
    partner_of_proposer = {prop: rec for rec, prop in assignments.items()}
    blocking_pairs = []
    for prop in proposer_prefs:
        for rec in receiver_prefs:
            if ranks_higher(proposer_prefs, prop, rec, partner_of_proposer.get(prop)) and ranks_higher(
                receiver_prefs, rec, prop, assignments.get(rec)
            ):
                blocking_pairs.append((prop, rec))
    return len(blocking_pairs) == 0, blocking_pairs


stable_matching = deferred_acceptance(PROPOSER_PREFS, RECEIVER_PREFS)
print("Stable?", check_stability(stable_matching, PROPOSER_PREFS, RECEIVER_PREFS))
print("Bad matching stable?", check_stability(TEST_BAD_MATCHING, PROPOSER_PREFS, RECEIVER_PREFS))
