"""
Scoreboard and HUD module for Neon Pong.
Features:
- Dual-player neon arcade scoreboard (Player 1 Cyan, Player 2 Pink)
- Real-time Rally Tracker with flame/lightning tiers and best-rally record
- Serve countdown announcer ("3... 2... 1... GO!")
- Point banners & Game Over victory screen with instant replay support ([R] to Restart)
- Pause overlay support
"""

from turtle import Turtle

class Scoreboard:
    def __init__(self, winning_score=7):
        self.l_score = 0
        self.r_score = 0
        self.winning_score = winning_score
        self.current_rally = 0
        self.best_rally = 0

        # Dedicated pen for persistent scores & header
        self.score_pen = Turtle()
        self.score_pen.hideturtle()
        self.score_pen.penup()
        self.score_pen.speed(0)

        # Dedicated pen for dynamic center banners (countdown, goals, game over)
        self.banner_pen = Turtle()
        self.banner_pen.hideturtle()
        self.banner_pen.penup()
        self.banner_pen.speed(0)

        self.update_scoreboard()

    def update_scoreboard(self):
        """Redraw scores, player headers, and current rally counter."""
        self.score_pen.clear()

        # Left Player (Player 1 - Cyan)
        self.score_pen.color("#00F5D4")
        self.score_pen.goto(-240, 310)
        self.score_pen.write("PLAYER 1", align="center", font=("Consolas", 13, "bold"))
        self.score_pen.goto(-240, 260)
        self.score_pen.write(f"{self.l_score:02d}", align="center", font=("Consolas", 38, "bold"))

        # Right Player (Player 2 - Pink)
        self.score_pen.color("#FF007F")
        self.score_pen.goto(240, 310)
        self.score_pen.write("PLAYER 2", align="center", font=("Consolas", 13, "bold"))
        self.score_pen.goto(240, 260)
        self.score_pen.write(f"{self.r_score:02d}", align="center", font=("Consolas", 38, "bold"))

        # Center Match info & Rally counter
        self.score_pen.color("#5A6B7C")
        self.score_pen.goto(0, 315)
        self.score_pen.write(f"FIRST TO {self.winning_score}", align="center", font=("Consolas", 11, "bold"))

        # Dynamic Rally Text
        self.score_pen.goto(0, 268)
        if self.current_rally >= 10:
            self.score_pen.color("#FF007F")
            rally_text = f"⚡ RALLY: {self.current_rally} ⚡"
        elif self.current_rally >= 5:
            self.score_pen.color("#FFE600")
            rally_text = f"🔥 RALLY: {self.current_rally} 🔥"
        elif self.current_rally > 0:
            self.score_pen.color("#00F5D4")
            rally_text = f"RALLY: {self.current_rally}"
        else:
            self.score_pen.color("#3D4852")
            rally_text = "RALLY: 0"

        if self.best_rally > 0:
            rally_text += f"  (BEST: {self.best_rally})"

        self.score_pen.write(rally_text, align="center", font=("Consolas", 12, "bold"))

    def update_rally(self, count: int):
        """Update rally streak and refresh HUD."""
        self.current_rally = count
        if self.current_rally > self.best_rally:
            self.best_rally = self.current_rally
        self.update_scoreboard()

    def increase_l_score(self):
        """Increment Left Player score."""
        self.l_score += 1
        self.current_rally = 0
        self.update_scoreboard()

    def increase_r_score(self):
        """Increment Right Player score."""
        self.r_score += 1
        self.current_rally = 0
        self.update_scoreboard()

    def check_winner(self):
        """Return winning player name or None."""
        if self.l_score >= self.winning_score:
            return "PLAYER 1"
        if self.r_score >= self.winning_score:
            return "PLAYER 2"
        return None

    def show_countdown(self, text: str):
        """Display serve countdown text at center court."""
        self.banner_pen.clear()
        self.banner_pen.color("#FFFFFF")
        self.banner_pen.goto(0, -35)
        self.banner_pen.write(text, align="center", font=("Consolas", 32, "bold"))

    def show_ready_to_serve(self, title: str = None, subtitle: str = "PRESS [ SPACE ] TO SERVE"):
        """Display paused ready-to-serve banner."""
        self.banner_pen.clear()
        if title:
            self.banner_pen.color("#00F5D4")
            self.banner_pen.goto(0, 30)
            self.banner_pen.write(title, align="center", font=("Consolas", 24, "bold"))
            self.banner_pen.color("#FFE600")
            self.banner_pen.goto(0, -25)
            self.banner_pen.write(subtitle, align="center", font=("Consolas", 15, "bold"))
        else:
            self.banner_pen.color("#FFE600")
            self.banner_pen.goto(0, -10)
            self.banner_pen.write(subtitle, align="center", font=("Consolas", 18, "bold"))

    def show_goal(self, scorer: str):
        """Display celebration banner when a point is scored and prompt to serve."""
        self.banner_pen.clear()
        color = "#00F5D4" if scorer == "PLAYER 1" else "#FF007F"
        self.banner_pen.color(color)
        self.banner_pen.goto(0, 30)
        self.banner_pen.write(f"★ POINT {scorer}! ★", align="center", font=("Consolas", 26, "bold"))

        self.banner_pen.color("#FFE600")
        self.banner_pen.goto(0, -25)
        self.banner_pen.write("PAUSED — PRESS [ SPACE ] TO SERVE", align="center", font=("Consolas", 14, "bold"))

    def show_winner(self, winner: str):
        """Display final victory banner with pause & restart prompt."""
        self.banner_pen.clear()
        color = "#00F5D4" if winner == "PLAYER 1" else "#FF007F"
        
        # Winner Title
        self.banner_pen.color(color)
        self.banner_pen.goto(0, 45)
        self.banner_pen.write(f"👑 {winner} WINS! 👑", align="center", font=("Consolas", 34, "bold"))

        # Final Score
        self.banner_pen.color("#FFFFFF")
        self.banner_pen.goto(0, -5)
        self.banner_pen.write(f"FINAL SCORE:  {self.l_score} - {self.r_score}", align="center", font=("Consolas", 19, "bold"))

        # Pause / Restart prompt
        self.banner_pen.color("#FFE600")
        self.banner_pen.goto(0, -55)
        self.banner_pen.write("— GAME OVER (PAUSED) —", align="center", font=("Consolas", 14, "bold"))

        self.banner_pen.color("#00F5D4")
        self.banner_pen.goto(0, -90)
        self.banner_pen.write("PRESS [ SPACE ] OR [ R ] TO RESTART   •   [ ESC ] TO QUIT", align="center", font=("Consolas", 12, "bold"))

    def show_paused(self):
        """Display paused status overlay."""
        self.banner_pen.clear()
        self.banner_pen.color("#FFE600")
        self.banner_pen.goto(0, 0)
        self.banner_pen.write("⏸  PAUSED", align="center", font=("Consolas", 36, "bold"))
        self.banner_pen.color("#A0AEC0")
        self.banner_pen.goto(0, -45)
        self.banner_pen.write("PRESS [ P ] TO RESUME", align="center", font=("Consolas", 16, "bold"))

    def clear_banner(self):
        """Clear temporary announcement banners."""
        self.banner_pen.clear()

    def reset_game(self):
        """Reset scores and banners for a fresh match."""
        self.l_score = 0
        self.r_score = 0
        self.current_rally = 0
        self.clear_banner()
        self.update_scoreboard()