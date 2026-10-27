"""
NEON PONG: CYBERPUNK EDITION
Main Game Controller

Features:
- 60 FPS fixed-timestep game loop
- Dynamic physics: angle calculation, paddle momentum/spin, velocity acceleration
- Visual juice: particle spark bursts, wall impact spray, goal fireworks, ball comet trails
- Squash & Stretch collision response
- Complete workable scoreboard with serve countdowns, rally combos, and match reset ([R])
- 8-bit sound effects (paddle hit pitch rise, wall bounce, scoring fanfare, victory tune)
- Turn pauses: Game pauses on round finish (goal) and GAME OVER, waiting for [SPACE] to serve/restart
"""

import time
import random
from turtle import Screen, Turtle

from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
from effects import EffectManager
import sound

# ----------------- Screen Configuration -----------------
screen = Screen()
canvas = screen.getcanvas()
root = canvas.winfo_toplevel()
root.resizable(False, False)

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title("NEON PONG: CYBERPUNK EDITION")
screen.bgcolor("#070913")
screen.tracer(0)

# Arena Boundaries
COURT_TOP = 240
COURT_BOTTOM = -280
COURT_CENTER_Y = (COURT_TOP + COURT_BOTTOM) // 2  # -20
PADDLE_MIN_Y = COURT_BOTTOM + 58                   # -222
PADDLE_MAX_Y = COURT_TOP - 58                      # 182
BALL_TOP_BOUND = COURT_TOP - 12                    # 228
BALL_BOTTOM_BOUND = COURT_BOTTOM + 12              # -268
GOAL_X_LIMIT = 425

# ----------------- Draw Arena Graphics -----------------
def draw_arena():
    pen = Turtle()
    pen.hideturtle()
    pen.penup()
    pen.speed(0)

    # 1. Center Court Ring
    pen.goto(0, COURT_CENTER_Y - 65)
    pen.color("#151D2A")
    pen.pensize(2)
    pen.pendown()
    pen.circle(65)
    pen.penup()

    # Center Spot
    pen.goto(0, COURT_CENTER_Y)
    pen.dot(8, "#1E293B")

    # 2. Dashed Divider Line
    pen.color("#233044")
    pen.pensize(3)
    pen.goto(0, COURT_TOP - 6)
    pen.setheading(270)
    for _ in range(16):
        pen.pendown()
        pen.forward(16)
        pen.penup()
        pen.forward(16)

    # 3. Top Glowing Boundary Bar (Dual Cyan/Pink)
    pen.pensize(4)
    # Left Cyan Half
    pen.color("#00F5D4")
    pen.goto(-425, COURT_TOP)
    pen.pendown()
    pen.goto(0, COURT_TOP)
    # Right Pink Half
    pen.color("#FF007F")
    pen.goto(425, COURT_TOP)
    pen.penup()

    # 4. Bottom Glowing Boundary Bar (Dual Cyan/Pink)
    # Left Cyan Half
    pen.color("#00F5D4")
    pen.goto(-425, COURT_BOTTOM)
    pen.pendown()
    pen.goto(0, COURT_BOTTOM)
    # Right Pink Half
    pen.color("#FF007F")
    pen.goto(425, COURT_BOTTOM)
    pen.penup()

    # 5. Footer Controls Hint
    pen.color("#4B5563")
    pen.goto(0, -325)
    pen.write("P1: [W] [S]    |    P2: [↑] [↓]    |    [SPACE]: SERVE / PAUSE    |    [R]: RESTART    |    [ESC]: QUIT",
              align="center", font=("Consolas", 10, "normal"))

draw_arena()

# ----------------- Game Entities -----------------
l_paddle = Paddle((-400, COURT_CENTER_Y), paddle_color="#00F5D4", min_y=PADDLE_MIN_Y, max_y=PADDLE_MAX_Y)
r_paddle = Paddle((400, COURT_CENTER_Y), paddle_color="#FF007F", min_y=PADDLE_MIN_Y, max_y=PADDLE_MAX_Y)
ball = Ball()
scoreboard = Scoreboard(winning_score=7)
effects = EffectManager()

# ----------------- State Machine -----------------
STATE_READY_TO_SERVE = "READY_TO_SERVE"
STATE_SERVE_COUNTDOWN = "SERVE_COUNTDOWN"
STATE_PLAYING = "PLAYING"
STATE_POINT_SCORED = "POINT_SCORED"
STATE_GAME_OVER = "GAME_OVER"

current_state = STATE_READY_TO_SERVE
countdown_step = 3
countdown_timer = 0
COUNTDOWN_INTERVAL = 24  # frames per step (~0.4s)

last_scorer = ""
next_serve_to_right = random.choice([True, False])

ball.reset(serve_to_right=next_serve_to_right, center_y=COURT_CENTER_Y)
scoreboard.show_ready_to_serve("NEON PONG", "PRESS [ SPACE ] TO SERVE")

# ----------------- Input Handling -----------------
keys = {"Up": False, "Down": False, "w": False, "s": False}
game_running = True
is_paused = False
restart_requested = False

def key_press(key):
    if key in keys:
        keys[key] = True

def key_release(key):
    if key in keys:
        keys[key] = False

def toggle_pause():
    global is_paused
    if current_state == STATE_PLAYING:
        is_paused = not is_paused
        if is_paused:
            scoreboard.show_paused()
        else:
            scoreboard.clear_banner()

def request_restart():
    global restart_requested
    restart_requested = True

def on_space_pressed():
    global current_state, countdown_step, countdown_timer, is_paused

    # If paused in active play, space toggles unpause
    if is_paused:
        toggle_pause()
        return

    # If game over, space restarts the match
    if current_state == STATE_GAME_OVER:
        request_restart()

    # If paused on point scored or initial launch, space begins the serve countdown
    elif current_state in (STATE_READY_TO_SERVE, STATE_POINT_SCORED):
        ball.reset(serve_to_right=next_serve_to_right, center_y=COURT_CENTER_Y)
        current_state = STATE_SERVE_COUNTDOWN
        countdown_step = 3
        countdown_timer = 0
        scoreboard.show_countdown("3")
        sound.sound_countdown(is_go=False)

    # If active playing, space pauses
    elif current_state == STATE_PLAYING:
        toggle_pause()

def quit_game():
    global game_running
    game_running = False

screen.listen()
# Player 2 controls
screen.onkeypress(lambda: key_press("Up"), "Up")
screen.onkeyrelease(lambda: key_release("Up"), "Up")
screen.onkeypress(lambda: key_press("Down"), "Down")
screen.onkeyrelease(lambda: key_release("Down"), "Down")

# Player 1 controls
screen.onkeypress(lambda: key_press("w"), "w")
screen.onkeyrelease(lambda: key_release("w"), "w")
screen.onkeypress(lambda: key_press("W"), "W")
screen.onkeyrelease(lambda: key_release("W"), "W")
screen.onkeypress(lambda: key_press("s"), "s")
screen.onkeyrelease(lambda: key_release("s"), "s")
screen.onkeypress(lambda: key_press("S"), "S")
screen.onkeyrelease(lambda: key_release("S"), "S")

# Space & Return to serve / unpause / restart
screen.onkeypress(on_space_pressed, "space")
screen.onkeypress(on_space_pressed, "Return")

# Hotkeys
screen.onkeypress(toggle_pause, "p")
screen.onkeypress(toggle_pause, "P")
screen.onkeypress(request_restart, "r")
screen.onkeypress(request_restart, "R")
screen.onkeypress(quit_game, "Escape")

# ----------------- Main Game Loop -----------------
TARGET_FPS = 60
FRAME_DURATION = 1.0 / TARGET_FPS

try:
    while game_running:
        frame_start = time.perf_counter()

        # Handle Pause during active play
        if is_paused:
            screen.update()
            time.sleep(0.03)
            continue

        # Handle Match Restart Request
        if restart_requested:
            restart_requested = False
            scoreboard.reset_game()
            effects.clear()
            next_serve_to_right = random.choice([True, False])
            ball.reset(serve_to_right=next_serve_to_right, center_y=COURT_CENTER_Y)
            current_state = STATE_READY_TO_SERVE
            scoreboard.show_ready_to_serve("NEW MATCH READY", "PRESS [ SPACE ] TO SERVE")

        # ---------------- State Logic ----------------
        if current_state in (STATE_READY_TO_SERVE, STATE_POINT_SCORED):
            # Ball stays stationary at center court until player presses [SPACE]
            ball.goto(0, COURT_CENTER_Y)

            # Allow players to position their paddles while paused
            if keys["w"]:
                l_paddle.go_up()
            if keys["s"]:
                l_paddle.go_down()
            if keys["Up"]:
                r_paddle.go_up()
            if keys["Down"]:
                r_paddle.go_down()

            l_paddle.update()
            r_paddle.update()

        elif current_state == STATE_SERVE_COUNTDOWN:
            # Ball stays centered during countdown
            ball.goto(0, COURT_CENTER_Y)
            countdown_timer += 1

            if countdown_timer >= COUNTDOWN_INTERVAL:
                countdown_timer = 0
                countdown_step -= 1

                if countdown_step == 2:
                    scoreboard.show_countdown("2")
                    sound.sound_countdown(is_go=False)
                elif countdown_step == 1:
                    scoreboard.show_countdown("1")
                    sound.sound_countdown(is_go=False)
                elif countdown_step == 0:
                    scoreboard.show_countdown("GO!")
                    sound.sound_countdown(is_go=True)
                elif countdown_step < 0:
                    scoreboard.clear_banner()
                    current_state = STATE_PLAYING

        elif current_state == STATE_PLAYING:
            # Paddle Movement Inputs
            if keys["w"]:
                l_paddle.go_up()
            if keys["s"]:
                l_paddle.go_down()
            if keys["Up"]:
                r_paddle.go_up()
            if keys["Down"]:
                r_paddle.go_down()

            l_paddle.update()
            r_paddle.update()

            # Advance Ball Physics
            ball.move()

            # Wall Collisions (Top & Bottom)
            wall_hit = ball.check_wall_collision(top_bound=BALL_TOP_BOUND, bottom_bound=BALL_BOTTOM_BOUND)
            if wall_hit != 0:
                sound.sound_wall_hit()
                effects.emit_wall_sparks(ball.xcor(), ball.ycor(), dir_y=wall_hit)

            # Paddle Collisions
            if ball.check_paddle_collision(l_paddle, is_left=True):
                sound.sound_paddle_hit(rally=ball.rally_count)
                effects.emit_paddle_sparks(ball.xcor(), ball.ycor(), dir_x=1, base_color="#00F5D4")
                scoreboard.update_rally(ball.rally_count)

            elif ball.check_paddle_collision(r_paddle, is_left=False):
                sound.sound_paddle_hit(rally=ball.rally_count)
                effects.emit_paddle_sparks(ball.xcor(), ball.ycor(), dir_x=-1, base_color="#FF007F")
                scoreboard.update_rally(ball.rally_count)

            # Goal Detection (Point Scored)
            if ball.xcor() > GOAL_X_LIMIT:
                # Left Player (Player 1) scores
                sound.sound_score()
                effects.emit_goal_explosion(ball.xcor(), ball.ycor())
                scoreboard.increase_l_score()
                last_scorer = "PLAYER 1"
                next_serve_to_right = False  # Serve towards the player who conceded

                winner = scoreboard.check_winner()
                if winner:
                    sound.sound_win()
                    scoreboard.show_winner(winner)
                    ball.clear_trail()
                    ball.goto(0, COURT_CENTER_Y)
                    current_state = STATE_GAME_OVER
                else:
                    # PAUSE on point scored! Wait for [SPACE] to serve
                    scoreboard.show_goal(last_scorer)
                    ball.clear_trail()
                    ball.goto(0, COURT_CENTER_Y)
                    current_state = STATE_POINT_SCORED

            elif ball.xcor() < -GOAL_X_LIMIT:
                # Right Player (Player 2) scores
                sound.sound_score()
                effects.emit_goal_explosion(ball.xcor(), ball.ycor())
                scoreboard.increase_r_score()
                last_scorer = "PLAYER 2"
                next_serve_to_right = True

                winner = scoreboard.check_winner()
                if winner:
                    sound.sound_win()
                    scoreboard.show_winner(winner)
                    ball.clear_trail()
                    ball.goto(0, COURT_CENTER_Y)
                    current_state = STATE_GAME_OVER
                else:
                    # PAUSE on point scored! Wait for [SPACE] to serve
                    scoreboard.show_goal(last_scorer)
                    ball.clear_trail()
                    ball.goto(0, COURT_CENTER_Y)
                    current_state = STATE_POINT_SCORED

        elif current_state == STATE_GAME_OVER:
            # Winner celebration: gentle continuous confetti fountain
            effects.emit_celebration(x=0, y=COURT_CENTER_Y, count=3)

        # Update and render particle physics
        effects.update_and_draw()

        # Render Frame
        screen.update()

        # Fixed 60 FPS frame throttle
        elapsed = time.perf_counter() - frame_start
        sleep_needed = FRAME_DURATION - elapsed
        if sleep_needed > 0:
            time.sleep(sleep_needed)

except Exception:
    pass

try:
    screen.bye()
except Exception:
    pass
