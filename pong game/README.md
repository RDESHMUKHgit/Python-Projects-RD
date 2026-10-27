# ⚡ Neon Pong: Cyberpunk Edition

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Library](https://img.shields.io/badge/Engine-Turtle%20Graphics-brightgreen?style=for-the-badge)](https://docs.python.org/3/library/turtle.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> A fast-paced, high-voltage reimagining of the classic 1972 Atari Pong, built entirely in Python using object-oriented principles, dynamic 2D physics, high-performance particle systems, and 8-bit retro audio.

---

## 🎮 Gameplay Preview & Highlights

- **🔥 Dynamic Angle & Spin Physics**: Hitting the ball near the paddle edge cuts sharp deflections (up to 55°), while paddle vertical motion transfers spin (*English*) to the ball.
- **⚡ Velocity Scaling**: Every rally return accelerates the ball, ramping up the intensity as volleys continue.
- **💫 Elastic Squash & Stretch**: Tactile visual impact deformations — the ball squashes horizontally on paddle strikes and vertically on wall bounces.
- **✨ Particle Systems**:
  - **Paddle Sparks**: Directional spark bursts spraying off the paddle face.
  - **Wall Dust**: Spark spray reflecting off top and bottom arena boundaries.
  - **Goal Fireworks**: Radial explosion of 45 multi-colored neon sparks when a goal is scored.
  - **Celebration Confetti**: Continuous confetti fountain for the match winner.
- **🌈 Dynamic Comet Trail**: Multi-stage fading particle trail that shifts colors as velocity escalates:
  - *Standard*: Ice Cyan (`#00F5D4`) & Deep Blue
  - *Fast*: Electric Yellow (`#FFE600`) & Lime
  - *Hyper Speed*: Blazing Neon Pink (`#FF007F`) & Violet
- **🎛️ Dual Scoreboard & Rally Tracker**:
  - Player 1 (Neon Cyan) and Player 2 (Hot Pink) digital score counters.
  - Live combo tracker (`RALLY: 5 🔥`, `⚡ RALLY: 10 ⚡ ULTRA RALLY!`) with high-rally record saving.
- **⏸️ Turn & Match Pauses**:
  - When a point is scored, the ball centers and **pauses**, prompting players to press `[SPACE]` to serve.
  - Serve countdown sequence (`3... 2... 1... GO!`) with audio sync.
  - Match winner screen (first to 7 points) with instant restart capability.
- **🔊 8-Bit Retro Audio**:
  - Non-blocking asynchronous audio effects with rising pitch on rallies (600 Hz – 1400 Hz), wall thuds, scoring chimes, and victory fanfares.

---

## 🕹️ Controls

| Action | Player 1 (Left - Cyan) | Player 2 (Right - Pink) |
|---|:---:|:---:|
| **Move Up** | `W` | `↑` (Up Arrow) |
| **Move Down** | `S` | `↓` (Down Arrow) |
| **Serve / Resume** | `[SPACE]` or `[ENTER]` | `[SPACE]` or `[ENTER]` |
| **Pause Game** | `P` or `[SPACE]` | `P` or `[SPACE]` |
| **Restart Match** | `R` | `R` |
| **Exit** | `ESC` | `ESC` |

---

## 📂 Project Structure

```text
pong-game/
├── main.py          # 60 FPS fixed-timestep game coordinator & arena renderer
├── ball.py          # Vector physics, angle deflection, squash-stretch & comet trail
├── paddle.py        # Clamped movement, momentum tracking & impact flash feedback
├── scoreboard.py    # Dual neon HUD, rally combo display & banner announcer
├── effects.py       # High-performance particle emitter (sparks, fireworks, confetti)
├── sound.py         # Thread-safe, non-blocking 8-bit retro audio generator
└── README.md        # Documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ installed (Windows, macOS, or Linux).
- Standard library only (`turtle`, `time`, `random`, `math`, `threading`, `winsound`). No external `pip` dependencies required!

### Run the Game
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/pong-game.git
   cd pong-game
   ```
2. Launch the game:
   ```bash
   python main.py
   ```

---

## 🛠️ Built With
- **Python 3** — Core game programming & state machine
- **Turtle Graphics** — Real-time 60 FPS vector canvas rendering
- **Tkinter** — Window & event loop management
- **Winsound / Threading** — Low-latency, non-blocking sound generation

---

## 📜 License
This project is licensed under the [MIT License](LICENSE). Feel free to modify, fork, and build upon it!

---

## 📬 Contact & Author

**Developed by — Rudraksh Deshmukh**  
- 📧 **Email:** rudraksha.d1234@gmail.com  
- 🔗 **LinkedIn:** [linkedin.com/in/rdworks](https://www.linkedin.com/in/rdworks)  

⭐ *If you enjoyed this project, please consider giving it a star on GitHub!*
