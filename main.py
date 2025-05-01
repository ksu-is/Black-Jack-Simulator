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

    if score == 21 and len(cards) == 2:
        return 0
    return score

def compare(player_score, computer_score):
    if player_score == computer_score:
        return "Draw"
    elif computer_score == 0:
        return "Lose, opponent has Blackjack!"
    elif player_score == 0:
        return "Win with a Blackjack!"
    elif player_score > 21:
        return "You went over. You lose!"
    elif computer_score > 21:
        return "Opponent went over. You win!"
    elif player_score > computer_score:
        return "You win!"
    else:
        return "You lose!"

def show_cards(player_cards, player_score, computer_cards, reveal_all=False):
    print("\nYour cards:", player_cards, "Current score:", player_score)
    if reveal_all:
        print("Computer's cards:", computer_cards, "Score:", calculate_score(computer_cards))
    else:
        print("Computer's first card:", computer_cards[0])

def play_game():
    print("\nWelcome to Blackjack!")

    player_cards = [deal_card(), deal_card()]
    computer_cards = [deal_card(), deal_card()]
    game_over = False

    while not game_over:
        player_score = calculate_score(player_cards)
        computer_score = calculate_score(computer_cards)
        show_cards(player_cards, player_score, computer_cards)

        if player_score == 0 or computer_score == 0 or player_score > 21:
            game_over = True
        else:
            draw = input("Type 'y' to get another card, type 'n' to pass: ")
            if draw.lower() == 'y':
                player_cards.append(deal_card())
            else:
                game_over = True

    while calculate_score(computer_cards) < 17:
        computer_cards.append(deal_card())

    player_score = calculate_score(player_cards)
    computer_score = calculate_score(computer_cards)

    show_cards(player_cards, player_score, computer_cards, reveal_all=True)
    print(compare(player_score, computer_score))

def main():
    while True:
        play = input("\nDo you want to play a game of Blackjack? Type 'y' or 'n': ")
        if play.lower() != 'y':
            print("Thanks for playing!")
            break
        play_game()

main()
