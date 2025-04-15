import random

def deal_card():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return random.choice(cards)
def calculate_score(cards):
    score = sum(cards)
    aces = cards.count(11)

    while score > 21 and aces:
        score -= 10 
        aces -= 1
