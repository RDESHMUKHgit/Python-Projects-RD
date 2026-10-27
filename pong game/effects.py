"""
Effects module for Neon Pong.
Provides high-performance particle systems:
- Paddle hit sparks
- Wall collision dust/sparks
- Goal explosion fireworks & confetti
- Winner celebration particle fountain
"""

from turtle import Turtle
import random
import math

NEON_COLORS = [
    "#00F5D4",  # Cyan
    "#7B2CBF",  # Purple
    "#FF007F",  # Pink
    "#FFE600",  # Yellow
    "#00FF66",  # Lime
    "#FF5400",  # Orange
    "#FFFFFF",  # Pure White
]

class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'color', 'size', 'life', 'max_life', 'gravity', 'drag')

    def __init__(self, x, y, vx, vy, color, size, life, gravity=0.0, drag=0.96):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.gravity = gravity
        self.drag = drag

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.drag
        self.vy = (self.vy * self.drag) - self.gravity
        self.life -= 1
        return self.life > 0

class EffectManager:
    def __init__(self):
        self.particles = []
        self.pen = Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.speed(0)

    def emit_paddle_sparks(self, x, y, dir_x, base_color="#00F5D4", count=16):
        """Emit sparks reflecting away from paddle face."""
        for _ in range(count):
            speed = random.uniform(3.0, 9.5)
            # Angle spread into the court (cone of +/- 45 degrees)
            angle = random.uniform(-0.8, 0.8)
            vx = dir_x * speed * math.cos(angle)
            vy = speed * math.sin(angle)
            color = random.choice([base_color, "#FFFFFF", "#FFE600"])
            size = random.uniform(3, 6)
            life = random.randint(10, 22)
            self.particles.append(Particle(x, y, vx, vy, color, size, life, gravity=0.05, drag=0.94))

    def emit_wall_sparks(self, x, y, dir_y, count=12):
        """Emit sparks bouncing off top or bottom arena borders."""
        for _ in range(count):
            speed = random.uniform(2.5, 7.5)
            angle = random.uniform(0.3, 2.8) if dir_y > 0 else random.uniform(-2.8, -0.3)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            color = random.choice(["#FFFFFF", "#00F5D4", "#FFE600", "#FF007F"])
            size = random.uniform(2, 5)
            life = random.randint(8, 18)
            self.particles.append(Particle(x, y, vx, vy, color, size, life, gravity=0.08, drag=0.93))

    def emit_goal_explosion(self, x, y, count=45):
        """Radial burst of colorful neon fireworks on a scored goal."""
        for _ in range(count):
            speed = random.uniform(3.0, 12.0)
            angle = random.uniform(0, 2 * math.pi)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            color = random.choice(NEON_COLORS)
            size = random.uniform(3, 7)
            life = random.randint(18, 38)
            self.particles.append(Particle(x, y, vx, vy, color, size, life, gravity=0.12, drag=0.95))

    def emit_celebration(self, x=0, y=0, count=10):
        """Continuous celebratory confetti for the match winner."""
        for _ in range(count):
            px = x + random.uniform(-250, 250)
            py = y + random.uniform(-100, 150)
            vx = random.uniform(-3, 3)
            vy = random.uniform(2, 8)
            color = random.choice(NEON_COLORS)
            size = random.uniform(3, 7)
            life = random.randint(25, 50)
            self.particles.append(Particle(px, py, vx, vy, color, size, life, gravity=0.15, drag=0.97))

    def update_and_draw(self):
        """Update physics and render all active particles."""
        if not self.particles:
            return

        self.pen.clear()
        surviving = []
        for p in self.particles:
            if p.update():
                # Render particle dot scaled by remaining life
                current_size = max(1, int(p.size * (p.life / p.max_life)))
                self.pen.goto(p.x, p.y)
                self.pen.dot(current_size, p.color)
                surviving.append(p)

        self.particles = surviving

    def clear(self):
        """Clear all active particles."""
        self.particles.clear()
        self.pen.clear()
