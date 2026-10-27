"""
Paddle module for Neon Pong.
Features:
- Smooth movement with boundary collision limits
- Velocity/Momentum tracking (transfers spin to ball)
- Visual impact flash (flashes white and thickens briefly when striking the ball)
"""

from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, position, paddle_color, min_y=-225, max_y=225):
        super().__init__()
        self.shape("square")
        self.base_width = 5.0
        self.base_len = 0.8
        self.shapesize(stretch_wid=self.base_width, stretch_len=self.base_len)
        self.base_color = paddle_color
        self.color(self.base_color)
        self.penup()
        self.goto(position)
        self.min_y = min_y
        self.max_y = max_y
        self.speed_step = 16.0
        self.dy = 0.0
        self.flash_timer = 0

    def go_up(self):
        new_y = min(self.ycor() + self.speed_step, self.max_y)
        self.dy = new_y - self.ycor()
        self.sety(new_y)

    def go_down(self):
        new_y = max(self.ycor() - self.speed_step, self.min_y)
        self.dy = new_y - self.ycor()
        self.sety(new_y)

    def flash(self):
        """Impact reaction: flashes bright white and thickens for punchy feedback."""
        self.flash_timer = 4
        self.color("#FFFFFF")
        self.shapesize(stretch_wid=self.base_width * 1.05, stretch_len=self.base_len * 1.4)

    def update(self):
        """Decay flash and momentum."""
        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer == 0:
                self.color(self.base_color)
                self.shapesize(stretch_wid=self.base_width, stretch_len=self.base_len)
        
        # Friction decay on momentum
        self.dy *= 0.5
