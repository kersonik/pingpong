# 🏓 Ping Pong Pygame

> A feature-rich, high-performance arcade Ping Pong game implemented in Python with Pygame, featuring intelligent predictive AI, local 2-player multiplayer, fixed-timestep physics, and a fully customizable settings menu.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Library](https://img.shields.io/badge/Engine-Pygame-yellow?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org/)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey?style=for-the-badge)](https://github.com/kersonik/pingpong)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

---

## 🕹️ Game Overview

```
=========================================
| [W/S]                          [▲/▼]  |
|   |                              |    |
|   |             o                |    |
|   |                              |    |
|  P1                             P2/AI |
=========================================
```

`pingpong` brings the legendary arcade table-tennis experience into modern Python with buttery-smooth physics, dynamic difficulty scaling, and a comprehensive configuration menu.

---

## ✨ Features & Highlights

- **🎮 Dual Game Modes**:
  - **Single Player (vs. AI)**: Play against a computer opponent that calculates wall bounces and trajectories in real time.
  - **Local 2-Player**: Compete head-to-head on the same keyboard.
- **🧠 Predictive AI with Adjustable Difficulties**:
  - **Easy**: Slower reaction speed and forgiving tracking offset.
  - **Medium**: Balanced challenge suitable for casual play.
  - **Hard**: Near-optimal bounce trajectory calculation with rapid interception.
- **⚙️ In-Game Configuration Menu**:
  - Target framerate toggle: `30 FPS`, `60 FPS`, or uncapped `120 FPS`.
  - Resolution selector & Fullscreen mode toggle.
  - Live FPS counter overlay.
- **⚡ Fixed-Timestep Physics**: Consistent game feel, paddle collision response, and ball motion regardless of monitor refresh rate or hardware performance.
- **🔥 Progressive Velocity Scaling**: Ball speed incrementally increases on each successful paddle return to maintain excitement.

---

## ⌨️ Controls & Keybindings

### Gameplay

| Action | Player 1 (Left Paddle) | Player 2 (Right Paddle) |
| :--- | :--- | :--- |
| **Move Up** | <kbd>W</kbd> | <kbd>▲</kbd> (Up Arrow) |
| **Move Down** | <kbd>S</kbd> | <kbd>▼</kbd> (Down Arrow) |

### Menu & General

| Key | Action |
| :--- | :--- |
| <kbd>▲</kbd> / <kbd>▼</kbd> or <kbd>W</kbd> / <kbd>S</kbd> | Navigate menu items |
| <kbd>Enter</kbd> | Select / Confirm option |
| <kbd>Escape</kbd> | Pause / Resume match, or return to previous menu |

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or newer
- `pip` package manager

### 1. Clone the Repository
```bash
git clone git@github.com:kersonik/pingpong.git
cd pingpong
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Game
```bash
python game.py
```

---

## 🧠 Physics & Mechanics

1. **Trajectory Prediction**: The AI does not cheat with instantaneous teleportation; it calculates bounce vectors against the top and bottom walls to determine the intercept point on the paddle's vertical axis, adding difficulty-dependent stochastic noise.
2. **Dynamic Resolution Scaling**: Paddle dimensions, velocity coefficients, and ball radius automatically rescale when toggling display resolutions, preserving identical physics feel at any screen size.
3. **Collision Reflection Angles**: Ball bounce angle varies based on the relative impact distance from the center of the paddle, allowing players to execute sharp angle shots.

---

## 📁 Repository Structure

```
pingpong/
├── game.py          # Complete game engine, menu state machine, AI and rendering
├── requirements.txt # Python package dependencies (pygame)
└── README.md        # Comprehensive game guide and instructions
```

---

## 📄 License

This project is licensed under the MIT License. Contributions and feedback are always welcome!
