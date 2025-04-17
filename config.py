from enum import Enum
from typing import Dict, Any
import json
import os


class Action(Enum):
    # Actions the agent can take
    STAY = 0
    JUMP = 1


class ObstacleType(Enum):
    # Types of obstacles in the game
    TREE = 1
    BIRD = 2


class GameConfig:
    # Default configuration values
    DEFAULTS = {
        "width": 20,
        "height": 2,
        "initial_agent_position": [0, 0],
        "episodes": 1000,
        "max_steps": 100,
        "learning_rate": 0.1,
        "discount_factor": 0.95,
        "initial_epsilon": 0.1,
        "min_epsilon": 0.01,
        "epsilon_decay": 0.995,
        "collision_reward": -100,
        "dodge_reward": 10,
        "survival_reward": 1,
        "render_delay": 0.1,
        "max_obstacles": 2,
        "agent_symbol": "@",
        "tree_symbol": "♧",
        "bird_symbol": "^",
        "collision_symbol": "☆",
        "empty_symbol": " "
    }

    def __init__(self, config_file: str = "game_config.json"):
        # Initialize config with defaults and load from file if exists
        self.config = self.DEFAULTS.copy()
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                self.config.update(json.load(file))

    def __getattr__(self, name: str) -> Any:
        # Allow attribute-style access to config values
        return self.config[name.lower()]

    def save(self, config_file: str = "game_config.json"):
        # Save current config to JSON file
        with open(config_file, "w") as file:
            json.dump(self.config, file, indent=2)
