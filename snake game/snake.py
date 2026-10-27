from turtle import Turtle

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
        self.can_turn = True

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)
        self.segments[0].color("#00FF88")  # Vibrant neon green head

    def add_segment(self, position):
        segment = Turtle("square")
        segment.shapesize(0.9, 0.9)  # Slight gap between segments looks modern
        segment.color("#E2E8F0")     # Sleek body color
        segment.penup()
        segment.goto(position)
        self.segments.append(segment)

    def extend(self):
        self.add_segment(self.segments[-1].position())

    def move(self):
        for seg in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg - 1].xcor()
            new_y = self.segments[seg - 1].ycor()
            self.segments[seg].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)
        self.can_turn = True

    def up(self):
        if self.can_turn and self.head.heading() != DOWN:
            self.head.setheading(UP)
            self.can_turn = False

    def down(self):
        if self.can_turn and self.head.heading() != UP:
            self.head.setheading(DOWN)
            self.can_turn = False

    def left(self):
        if self.can_turn and self.head.heading() != RIGHT:
            self.head.setheading(LEFT)
            self.can_turn = False

    def right(self):
        if self.can_turn and self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
            self.can_turn = False

    def reset(self):
        for seg in self.segments:
            seg.goto(1000, 1000)
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]
        self.can_turn = True
