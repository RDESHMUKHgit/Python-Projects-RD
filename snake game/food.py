from turtle import Turtle
import random

FOOD_COLORS = ["#FF3366", "#FFE600", "#00F5D4", "#FF6B00", "#A06CD5"]

class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(0.7, 0.7)
        self.color(random.choice(FOOD_COLORS))
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        """Place food at a random grid-aligned position and pick a vibrant color."""
        # Grid aligned within boundaries (-260 to 240)
        rand_x = random.randint(-13, 13) * 20
        rand_y = random.randint(-13, 11) * 20
        self.color(random.choice(FOOD_COLORS))
        self.goto(rand_x, rand_y)