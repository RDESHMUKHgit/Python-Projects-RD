import time
import threading
from turtle import Screen, Turtle

from snake import Snake
from food import Food
from scoreboard import Scoreboard

# Optional lightweight sound
try:
    import winsound
    def play_sound(freq, duration):
        threading.Thread(target=lambda: winsound.Beep(freq, duration), daemon=True).start()
except ImportError:
    def play_sound(freq, duration):
        pass

# ----------------- Screen Setup -----------------
screen = Screen()
canvas = screen.getcanvas()
root = canvas.winfo_toplevel()
root.resizable(False, False)

screen.setup(width=620, height=620)
screen.bgcolor("#0B0F19")
screen.title("Cyber Snake Game")
screen.tracer(0)

# ----------------- Draw Arena Border -----------------
def draw_border():
    border = Turtle()
    border.hideturtle()
    border.penup()
    border.color("#1E293B")
    border.pensize(3)
    
    # Outer arena boundary box
    border.goto(-285, -285)
    border.pendown()
    for _ in range(2):
        border.forward(570)
        border.left(90)
        border.forward(540)
        border.left(90)
    border.penup()

draw_border()

# ----------------- Game Entities -----------------
snake = Snake()
food = Food()
score = Scoreboard()

# ----------------- Game State -----------------
game_running = True
is_game_over = False
is_paused = False

def restart_game():
    global is_game_over, is_paused
    if is_game_over:
        is_game_over = False
        snake.reset()
        score.reset_score()
        food.refresh()

def toggle_pause():
    global is_paused
    if not is_game_over:
        is_paused = not is_paused

def on_space_pressed():
    if is_game_over:
        restart_game()
    else:
        toggle_pause()

# ----------------- Input Key Bindings -----------------
screen.listen()
# Arrow keys
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

# WASD keys
screen.onkey(snake.up, "w")
screen.onkey(snake.up, "W")
screen.onkey(snake.down, "s")
screen.onkey(snake.down, "S")
screen.onkey(snake.left, "a")
screen.onkey(snake.left, "A")
screen.onkey(snake.right, "d")
screen.onkey(snake.right, "D")

# Space & Hotkeys
screen.onkey(on_space_pressed, "space")
screen.onkey(restart_game, "r")
screen.onkey(restart_game, "R")
screen.onkey(toggle_pause, "p")
screen.onkey(toggle_pause, "P")

# ----------------- Main Game Loop -----------------
WALL_RIGHT = 280
WALL_LEFT = -280
WALL_TOP = 250
WALL_BOTTOM = -280

try:
    while game_running:
        screen.update()
        time.sleep(0.085)

        if is_paused or is_game_over:
            continue

        snake.move()

        # 1. Detect collision with food
        if snake.head.distance(food) < 18:
            food.refresh()
            score.increase_score()
            snake.extend()
            play_sound(750, 30)

        # 2. Detect collision with wall
        head_x = snake.head.xcor()
        head_y = snake.head.ycor()
        if head_x > WALL_RIGHT or head_x < WALL_LEFT or head_y > WALL_TOP or head_y < WALL_BOTTOM:
            is_game_over = True
            play_sound(240, 90)
            score.gameOver()

        # 3. Detect collision with own tail
        for segment in snake.segments[1:]:
            if snake.head.distance(segment) < 12:
                is_game_over = True
                play_sound(240, 90)
                score.gameOver()
                break

except Exception:
    pass

try:
    screen.bye()
except Exception:
    pass
