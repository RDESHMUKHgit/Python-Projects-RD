"""
Ball module for Neon Pong.
Features:
- Accurate angle reflection based on paddle impact zone
- Paddle spin / English physics transfer from paddle motion
- Squash & stretch elasticity on collisions
- Dynamic neon color transitions based on rally & speed
- High-performance glowing comet trail
"""

from turtle import Turtle
import math
import random

COLOR_TIERS = [
    (10.0, "#00F5D4", ["#002b36", "#004b5c", "#008299", "#00B4D8", "#00F5D4"]),  # Cyan
    (13.5, "#FFE600", ["#2d2700", "#5c5000", "#998500", "#cca800", "#FFE600"]),  # Electric Yellow
    (99.0, "#FF007F", ["#36001a", "#6b0034", "#a3004f", "#d60068", "#FF007F"]),  # Hyper Pink
]

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.base_color = "#00F5D4"
        self.color(self.base_color)

        self.base_speed = 8.0
        self.speed = self.base_speed
        self.max_speed = 18.0
        self.vx = self.base_speed
        self.vy = 0.0

        # Squash and stretch state
        self.squash_counter = 0
        self.current_wid = 1.0
        self.current_len = 1.0

        # Rally tracking
        self.rally_count = 0

        # Comet trail pen & history
        self.trail_pen = Turtle()
        self.trail_pen.hideturtle()
        self.trail_pen.penup()
        self.trail_pen.speed(0)
        self.positions = []
        self.max_trail = 7

        self.reset(serve_to_right=random.choice([True, False]))

    def get_tier_info(self):
        """Return (ball_color, trail_palette) based on current velocity."""
        for speed_cap, col, palette in COLOR_TIERS:
            if self.speed <= speed_cap:
                return col, palette
        return COLOR_TIERS[-1][1], COLOR_TIERS[-1][2]

    def move(self):
        """Update position, trail, and squash-stretch recovery."""
        # Record trail position
        self.positions.append((self.xcor(), self.ycor()))
        if len(self.positions) > self.max_trail:
            self.positions.pop(0)

        # Draw glowing comet trail
        ball_color, palette = self.get_tier_info()
        self.color(ball_color)

        self.trail_pen.clear()
        num_pos = len(self.positions)
        for i, (tx, ty) in enumerate(self.positions):
            # Scale dot size and color towards recent positions
            size = int(3 + (i / max(1, num_pos - 1)) * 9)
            color_idx = min(int((i / max(1, num_pos)) * len(palette)), len(palette) - 1)
            self.trail_pen.goto(tx, ty)
            self.trail_pen.dot(size, palette[color_idx])

        # Step ball position
        self.goto(self.xcor() + self.vx, self.ycor() + self.vy)

        # Elastic recovery from squash/stretch
        if self.squash_counter > 0:
            self.squash_counter -= 1
            # Smoothly interpolate back to (1.0, 1.0)
            self.current_wid += (1.0 - self.current_wid) * 0.35
            self.current_len += (1.0 - self.current_len) * 0.35
            self.shapesize(stretch_wid=self.current_wid, stretch_len=self.current_len)
        else:
            self.shapesize(1.0, 1.0)

    def trigger_squash(self, wid: float, length: float, frames: int = 5):
        """Apply squash & stretch deformation."""
        self.current_wid = wid
        self.current_len = length
        self.squash_counter = frames
        self.shapesize(stretch_wid=wid, stretch_len=length)

    def check_wall_collision(self, top_bound: float = 270, bottom_bound: float = -270):
        """
        Bounce ball off top or bottom arena borders with elasticity.
        Returns:
            +1 if bounced off bottom wall,
            -1 if bounced off top wall,
            0 if no wall collision.
        """
        if self.ycor() >= top_bound:
            self.sety(top_bound)
            self.vy = -abs(self.vy)
            self.trigger_squash(wid=0.6, length=1.45)
            return -1
        elif self.ycor() <= bottom_bound:
            self.sety(bottom_bound)
            self.vy = abs(self.vy)
            self.trigger_squash(wid=0.6, length=1.45)
            return 1
        return 0

    def check_paddle_collision(self, paddle, is_left: bool):
        """
        Check collision with paddle, applying angle reflection and momentum spin.
        Returns True if a bounce occurred.
        """
        pad_x = paddle.xcor()
        pad_y = paddle.ycor()

        # Check bounds: paddle width is ~16 (x +/- 15), height is 100 (y +/- 55)
        if is_left:
            # Ball moving left, striking left paddle face
            is_in_x = (pad_x - 10 <= self.xcor() <= pad_x + 22) and self.vx < 0
        else:
            # Ball moving right, striking right paddle face
            is_in_x = (pad_x - 22 <= self.xcor() <= pad_x + 10) and self.vx > 0

        is_in_y = abs(self.ycor() - pad_y) <= 56

        if is_in_x and is_in_y:
            # Normalized impact offset from center (-1.0 at bottom tip, +1.0 at top tip)
            offset = (self.ycor() - pad_y) / 50.0
            offset = max(-1.0, min(1.0, offset))

            # Base reflection angle (up to 55 degrees)
            angle = offset * math.radians(55)

            # Apply spin / English from paddle motion
            angle += paddle.dy * 0.015

            # Clamp angle to prevent purely vertical bounces
            max_ang = math.radians(72)
            angle = max(-max_ang, min(max_ang, angle))

            # Increase speed on return
            self.speed = min(self.speed * 1.06, self.max_speed)
            self.rally_count += 1

            dir_x = 1 if is_left else -1
            self.vx = dir_x * self.speed * math.cos(angle)
            self.vy = self.speed * math.sin(angle)

            # Push ball out of paddle to avoid multi-collision tunneling
            if is_left:
                self.setx(pad_x + 20)
            else:
                self.setx(pad_x - 20)

            # Trigger horizontal squash & vertical stretch
            self.trigger_squash(wid=1.45, length=0.6)
            paddle.flash()
            return True

        return False

    def reset(self, serve_to_right: bool = True, center_y: float = -20):
        """Reset ball to center court for a new serve."""
        self.goto(0, center_y)
        self.speed = self.base_speed
        self.rally_count = 0
        self.positions.clear()
        self.trail_pen.clear()
        self.squash_counter = 0
        self.shapesize(1.0, 1.0)

        # Serve at slight random angle
        serve_angle = random.uniform(-math.radians(25), math.radians(25))
        dir_x = 1 if serve_to_right else -1
        self.vx = dir_x * self.speed * math.cos(serve_angle)
        self.vy = self.speed * math.sin(serve_angle)

        col, _ = self.get_tier_info()
        self.color(col)

    def clear_trail(self):
        """Clear all visual trail remnants."""
        self.positions.clear()
        self.trail_pen.clear()
