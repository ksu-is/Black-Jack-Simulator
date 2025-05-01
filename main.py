import random
import tkinter as tk
from PIL import Image, ImageTk
import os

CARD_FOLDER = "cards"
CARD_WIDTH = 80
CARD_HEIGHT = 120

card_mapping = {
    2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
    11: "ace"
}

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

class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Table")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="green")
        self.canvas.pack()

        self.total_label = tk.Label(root, text="", font=("Helvetica", 14), bg="green", fg="white")
        self.total_label.place(x=300, y=10)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 16), bg="green", fg="yellow")
        self.result_label.place(x=280, y=550)

        self.hit_button = tk.Button(root, text="Hit", font=("Helvetica", 14), command=self.hit)
        self.hit_button.pack(side="left", padx=20, pady=20)

        self.stand_button = tk.Button(root, text="Stand", font=("Helvetica", 14), command=self.stand)
        self.stand_button.pack(side="right", padx=20, pady=20)

        self.play_again_button = tk.Button(root, text="Play Again", font=("Helvetica", 14), command=self.start_new_game)
        self.play_again_button.place(x=330, y=510)
        self.play_again_button.lower()

        self.card_images = {}
        self.image_refs = []
        self.reveal_dealer = False

        # NEW: Track visual image name per card
        self.player_card_faces = []
        self.dealer_card_faces = []

        self.reset_game()
        self.start_new_game()

    def reset_game(self):
        self.player_cards = []
        self.dealer_cards = []
        self.player_card_faces = []
        self.dealer_card_faces = []
        self.game_over = False
        self.reveal_dealer = False
        self.result_label.config(text="")
        self.play_again_button.lower()
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")

    def start_new_game(self):
        self.reset_game()
        self.add_player_card(deal_card())
        self.add_player_card(deal_card())
        self.add_dealer_card(deal_card())
        self.add_dealer_card(deal_card())
        self.update_canvas()

    def add_player_card(self, value):
        self.player_cards.append(value)
        self.player_card_faces.append(self.get_card_filename(value))

    def add_dealer_card(self, value):
        self.dealer_cards.append(value)
        self.dealer_card_faces.append(self.get_card_filename(value))

    def get_card_filename(self, value):
        if value == 10:
            return random.choice(["jack.png", "queen.png", "king.png"])
        else:
            return f"{card_mapping.get(value, '10')}.png"

    def load_card_image(self, file_name):
        path = os.path.join(CARD_FOLDER, file_name)
        if path not in self.card_images:
            image = Image.open(path).resize((CARD_WIDTH, CARD_HEIGHT))
            self.card_images[path] = ImageTk.PhotoImage(image)
        return self.card_images[path]

    def update_canvas(self):
        self.canvas.delete("all")
        self.image_refs.clear()

        for i, (value, face) in enumerate(zip(self.dealer_cards, self.dealer_card_faces)):
            if i == 1 and not self.reveal_dealer:
                img = self.load_card_image("back.png")
            else:
                img = self.load_card_image(face)
            self.canvas.create_image(100 + i * (CARD_WIDTH + 10), 100, image=img, anchor="nw")
            self.image_refs.append(img)

        for i, face in enumerate(self.player_card_faces):
            img = self.load_card_image(face)
            self.canvas.create_image(100 + i * (CARD_WIDTH + 10), 350, image=img, anchor="nw")
            self.image_refs.append(img)

        player_score = calculate_score(self.player_cards)
        dealer_score = calculate_score(self.dealer_cards) if self.reveal_dealer else "??"
        self.total_label.config(text=f"Your total: {player_score}     Dealer total: {dealer_score}")

    def hit(self):
        if self.game_over:
            return
        value = deal_card()
        self.add_player_card(value)
        if calculate_score(self.player_cards) > 21:
            self.end_game()
        self.update_canvas()

    def stand(self):
        if self.game_over:
            return
        self.reveal_dealer = True
        while calculate_score(self.dealer_cards) < 17:
            value = deal_card()
            self.add_dealer_card(value)
        self.end_game()

    def end_game(self):
        self.game_over = True
        self.update_canvas()
        result = compare(calculate_score(self.player_cards), calculate_score(self.dealer_cards))
        self.result_label.config(text=result)
        self.play_again_button.lift()
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackApp(root)
    root.mainloop()
