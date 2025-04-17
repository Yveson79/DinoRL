# 🦖 DinoRL

**DinoRL** is a 2D Q-learning-based game where an agent learns to avoid obstacles (like trees and birds) on a simple grid. The project serves as a practical introduction to *Reinforcement Learning* concepts, with an interactive and customizable interface.

![DinoRL Screenshot](imag.png)

---

## 🚀 Key Features

- 🧠 **Q-learning**: Reinforcement learning algorithm used to train the agent to dodge obstacles.
- 🎮 **Interactive Menu**: Train, test, save/load the agent’s state, and manage game settings.
- 🌪️ **Dynamic Challenges**: Support for multiple obstacles to increase difficulty.
- 📊 **Progress Bars**: Visual feedback for training/testing using `tqdm`.
- ⚙️ **JSON Configuration**: Fully customizable via `game_config.json`.
- 📝 **Detailed Logging**: Logs written both to the console and to `game.log`.

---

## 🗂️ Project Structure

```text
├── agent.py         # Q-learning agent logic and state management
├── config.py        # Game configuration and enums
├── environment.py   # Grid management, agent, and obstacle logic
├── main.py          # Main interface with menu
├── renderer.py      # Console-based rendering of the game state
├── requirements.txt # List of dependencies
├── game.log         # Log file generated during execution
├── imag.png         # Game screenshot or illustration
└── LICENSE.txt      # Project license (MIT)
```

---

## 📦 Prerequisites

- Python 3.6 or higher  
- A terminal with UTF-8 support  
- (Optional) Virtual environment for isolated dependencies

---

## ⚙️ Setup

1. **Clone or navigate to the project directory**:
   ```bash
   DinoRL/
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:  
   Make sure your `requirements.txt` includes:
   ```
   tqdm>=4.66.5
   numpy>=1.26.4
   ```
   Then run:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Game

1. **Run the main script**:
   ```bash
   python main.py
   ```

2. **Use the interactive menu to**:
   - **Train Agent**: Train for a custom number of episodes (default: 1000)
   - **Test Agent**: Run test episodes (default: 1)
   - **Save Agent State**: Save Q-table and epsilon to `agent_state.json`
   - **Load Agent State**: Load a previously saved agent state
   - **Save Configuration**: Generate or update `game_config.json`
   - **Exit**: Quit the program

---

## 🛠️ Customizing the Game

The `game_config.json` file (created after saving configuration) allows you to tweak:

- `width`, `height`: Grid dimensions  
- `max_obstacles`: Max number of simultaneous obstacles  
- `learning_rate`, `discount_factor`: Q-learning hyperparameters  
- `render_delay`: Time between frames (default: 0.1 seconds)

---

## 📋 Logging

- Logs are written to `game.log` and shown in the terminal.
- Includes: episode summaries, saving/loading events, and errors.
- To enable *debug logging*, edit the `setup_logging` function in `main.py` and set:
  ```python
  level=logging.DEBUG
  ```

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

