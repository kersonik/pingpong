# Ping Pong Pygame

A classic, fully functional Ping Pong game implemented in Python using the `pygame` library. It features both single-player (vs. AI) and two-player modes, along with a configurable settings menu.

## Features
*   **Dual Modes:** Choose between playing against a smart AI or a local 2-player match.
*   **Settings Menu:** 
    *   AI Difficulty selection (Easy, Medium, Hard).
    *   Configurable FPS (30, 60, 120).
    *   Resolution and Fullscreen toggle.
    *   FPS Overlay for performance monitoring.
*   **Responsive Gameplay:** Uses fixed-timestep logic for consistent performance across different hardware.
*   **Progressive Difficulty:** The ball accelerates over time, increasing the challenge as the match goes on.

## Requirements
*   Python 3.x
*   `pygame` library

To install the dependency, run:
```bash
pip install pygame
```

## How to Play
*   **Run the script:**
    ```bash
    python main.py
    ``` 

*   **Menu Navigation:**
    *   Use **↑/↓** or **W/S** keys to move between options.
    *   Press **Enter** to select.
    *   Press **Esc** to return to the menu or pause/resume the game.
*   **Controls:**
    *   **Left Player:** W (Up) / S (Down).
    *   **Right Player (2P mode):** Up Arrow / Down Arrow.

## Gameplay Mechanics
*   **AI Logic:** The AI calculates the ball's trajectory (including wall bounces) and attempts to intercept it with a difficulty-based error margin.
*   **Speed:** The game dynamically adjusts speeds based on the selected resolution to ensure the game feel remains consistent regardless of the screen size.
