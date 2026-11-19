# Stores and displays ranked preference lists for both sides of a matching market.

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

print("Student preferences:", PROPOSER_PREFS)
print("University preferences:", RECEIVER_PREFS)
