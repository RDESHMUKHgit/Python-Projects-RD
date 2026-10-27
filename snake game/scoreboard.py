import os
from turtle import Turtle

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.txt")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.high_score = self.load_high_score()
        self.update_scoreboard()

    def load_high_score(self):
        """Safely read high score from local data.txt."""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, mode="r") as file:
                    content = file.read().strip()
                    if content.isdigit():
                        return int(content)
        except Exception:
            pass
        return 0

    def save_high_score(self):
        """Safely persist high score to local data.txt."""
        try:
            with open(DATA_FILE, mode="w") as file:
                file.write(str(self.high_score))
        except Exception:
            pass

    def update_scoreboard(self):
        self.clear()
        self.goto(0, 260)
        self.color("#00F5D4")
        self.write(f"SCORE: {self.score}   |   HIGH SCORE: {self.high_score}",
                   align="center", font=("Consolas", 14, "bold"))

    def increase_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.update_scoreboard()

    def gameOver(self):
        self.goto(0, 30)
        self.color("#FF0055")
        self.write("GAME OVER", align="center", font=("Consolas", 36, "bold"))
        self.goto(0, -20)
        self.color("#FFE600")
        self.write("PRESS [ SPACE ] OR [ R ] TO PLAY AGAIN", align="center", font=("Consolas", 13, "bold"))

    def reset_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.score = 0
        self.update_scoreboard()