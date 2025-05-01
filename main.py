import random
import tkinter as tk
from tkinter import messagebox


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

def compare(player_score, dealer_score):
    if player_score == dealer_score:
        return "Draw"
    elif dealer_score == 0:
        return "You lose, dealer has Blackjack!"
    elif player_score == 0:
        return "Blackjack! You win!"
    elif player_score > 21:
        return "You went over. You lose!"
    elif dealer_score > 21:
        return "Dealer went over. You win!"
    elif player_score > dealer_score:
        return "You win!"
    else:
        return "You lose!"

def get_dealer_total(cards):
    return calculate_score(cards)

# ---------- GUI App ----------

class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")

        self.root.configure(bg="#0B3D0B") 

        self.reset_game()

        self.frame = tk.Frame(root, bg="#0B3D0B")
        self.frame.pack(padx=20, pady=20)

        self.info_label = tk.Label(self.frame, text="♠️ Welcome to Blackjack ♣️",
                                   font=("Helvetica", 22, "bold"),
                                   bg="#0B3D0B", fg="gold")  
        self.info_label.pack(pady=15)

    
        self.player_label = tk.Label(self.frame, text="", font=("Helvetica", 16),
                                     bg="#0B3D0B", fg="white")
        self.player_label.pack(pady=10)

        self.dealer_label = tk.Label(self.frame, text="", font=("Helvetica", 16),
                                     bg="#0B3D0B", fg="white")
        self.dealer_label.pack(pady=10)

        self.button_frame = tk.Frame(self.frame, bg="#0B3D0B")
        self.button_frame.pack(pady=15)

        self.hit_button = tk.Button(self.button_frame, text="Hit", font=("Helvetica", 14, "bold"),
                                    bg="#228B22", fg="white", activebackground="#2E8B57",
                                    width=12, height=2, command=self.hit)
        self.hit_button.pack(side="left", padx=20)

        self.stand_button = tk.Button(self.button_frame, text="Stand", font=("Helvetica", 14, "bold"),
                                      bg="#228B22", fg="white", activebackground="#2E8B57",
                                      width=12, height=2, command=self.stand)
        self.stand_button.pack(side="right", padx=20)

        self.start_new_game()

    def reset_game(self):
        self.player_cards = []
        self.dealer_cards = []
        self.game_over = False

    def start_new_game(self):
        self.reset_game()
        self.player_cards = [deal_card(), deal_card()]
        self.dealer_cards = [deal_card(), deal_card()]
        self.update_labels()

    def update_labels(self, reveal_dealer=False):
        player_score = calculate_score(self.player_cards)

        if reveal_dealer:
            dealer_score = get_dealer_total(self.dealer_cards)  
            dealer_display = self.dealer_cards
            self.dealer_label.config(
                text=f"Dealer's Hand: {dealer_display} | Score: {dealer_score}"  
            )
        else:
            dealer_display = [self.dealer_cards[0], "?"]
            self.dealer_label.config(
                text=f"Dealer's Hand: {dealer_display}"  
            )

        self.player_label.config(
            text=f"Your Hand: {self.player_cards} | Score: {player_score}"  
        )
    def hit(self):
        if self.game_over:
            return

        self.player_cards.append(deal_card())
        player_score = calculate_score(self.player_cards)
        self.update_labels()

        if player_score > 21:
            self.end_game()

    def stand(self):
        if self.game_over:
            return

        while calculate_score(self.dealer_cards) < 17:
            self.dealer_cards.append(deal_card())

        self.end_game()

    def end_game(self):
        self.game_over = True
        player_score = calculate_score(self.player_cards)
        dealer_score = calculate_score(self.dealer_cards)

        self.update_labels(reveal_dealer=True)
        result = compare(player_score, dealer_score)
        messagebox.showinfo("Game Over", result)
        self.ask_replay()

    def ask_replay(self):
        if messagebox.askyesno("Play Again", "Do you want to play again?"):
            self.start_new_game()
        else:
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackApp(root)
    root.mainloop()
