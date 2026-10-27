# 🐍 Cyber Snake Game (Turtle Edition)

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Library](https://img.shields.io/badge/Engine-Turtle%20Graphics-brightgreen?style=for-the-badge)](https://docs.python.org/3/library/turtle.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> A sleek, arcade-style edition of the classic Snake Game, built entirely in Python using object-oriented architecture, persistent high-score tracking, grid-aligned kinematics, and retro audio.

---

## 🚀 Key Features

- **🕹️ Classic & Responsive Gameplay**: Eat food, grow longer, avoid arena boundary walls, and dodge your own tail.
- **💾 Persistent High-Score Tracking**: Reads and stores your best record in a local `data.txt` file with safe dynamic path resolution.
- **🍎 Color-Cycling Food**: Food spawns randomly across a 20px snapped grid and cycles through bright fruit palettes (`#FF3366`, `#FFE600`, `#00F5D4`, `#FF6B00`, `#A06CD5`).
- **🛡️ Rapid-Turn Lockout Protection**: Built-in direction lock prevents 180° instant turns, eliminating accidental neck collisions when hitting keys quickly.
- **🟩 Modern Aesthetic**: Neon green snake head (`#00FF88`), sleek body segments, dark cyberpunk arena background (`#0B0F19`), and a crisp boundary wall box.
- **🔄 Instant Replay Loop**: When game over occurs, press **`[SPACE]`** or **`[R]`** to instantly start a new match without closing the window.
- **⏸️ Pause & Resume**: Hit **`P`** or **`[SPACE]`** anytime during gameplay to pause the action.
- **🔊 8-Bit Retro Audio**: Non-blocking audio beeps on food capture (750 Hz) and crash thuds (240 Hz).

---

## 🕹️ Controls

| Action | Primary Keys | Alternative Keys |
|---|:---:|:---:|
| **Move Up** | `↑` (Up Arrow) | `W` |
| **Move Down** | `↓` (Down Arrow) | `S` |
| **Move Left** | `←` (Left Arrow) | `A` |
| **Move Right** | `→` (Right Arrow) | `D` |
| **Pause / Resume** | `P` | `[SPACE]` |
| **Restart (on Game Over)** | `[SPACE]` | `R` |

---

## 📂 Project Structure

```text
snake-game/
├── main.py          # Main game loop, collision detection & arena boundary setup
├── snake.py         # Snake segments, body extension, kinematics & turn lockout
├── food.py          # Grid-aligned food spawner with dynamic color cycling
├── scoreboard.py    # Score & High-score HUD with persistent file storage
├── data.txt         # Local persistent high-score record
└── README.md        # Documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ installed (Windows, macOS, or Linux).
- Standard library only (`turtle`, `time`, `random`, `os`, `threading`, `winsound`). No external `pip` packages required!

### Run the Game
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/snake-game.git
   cd snake-game
   ```
2. Launch the game:
   ```bash
   python main.py
   ```

---

## 🛠️ Built With
- **Python 3** — Core game programming & OOP design
- **Turtle Graphics** — Real-time 2D vector canvas rendering
- **Tkinter** — Window event management
- **Winsound / Threading** — Low-latency retro sound effects

---

## 📜 License
This project is licensed under the [MIT License](LICENSE). Feel free to modify, fork, and distribute it — just give proper credit.

---

## 📬 Contact & Author

**Developed by — Rudraksh Deshmukh**  
- 📧 **Email:** rudraksha.d1234@gmail.com  
- 🔗 **LinkedIn:** [linkedin.com/in/rdworks](https://www.linkedin.com/in/rdworks)  

⭐ *If you enjoyed this project, don't forget to give it a star on GitHub!*
