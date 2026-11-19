# Computes a stable two-sided matching using the Gale-Shapley deferred acceptance algorithm.

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


result_matching = deferred_acceptance(PROPOSER_PREFS, RECEIVER_PREFS)
print("Matching:", result_matching)
