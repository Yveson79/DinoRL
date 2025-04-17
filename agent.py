from typing import Tuple, Dict, List
import random
import json
import os
import numpy as np
from config import GameConfig, Action
from environment import GameEnvironment
import logging


class QLearningAgent:
    def __init__(self, environment: GameEnvironment, config: GameConfig):
        # Initialize agent with environment, config, and logger
        self.environment = environment
        self.config = config
        self.q_table: Dict[Tuple[int, int, int], List[float]] = {}
        self.epsilon = config.initial_epsilon
        self.logger = logging.getLogger(__name__)

    def get_q_values(self, state: Tuple[int, int, int]) -> List[float]:
        # Retrieve or initialize Q-values for a state
        return self.q_table.setdefault(state, [0.0] * len(Action))

    def choose_action(self, state: Tuple[int, int, int], explore: bool = True) -> int:
        # Choose action: random if exploring, otherwise best Q-value
        if explore and random.random() < self.epsilon:
            return random.choice([action.value for action in Action])
        return int(np.argmax(self.get_q_values(state)))

    def update_q_table(self, state: Tuple[int, int, int], action: int, reward: float, next_state: Tuple[int, int, int]):
        # Update Q-table using Q-learning formula
        best_next_action = int(np.argmax(self.get_q_values(next_state)))
        current_q = self.get_q_values(state)[action]
        target_q = reward + self.config.discount_factor * self.get_q_values(next_state)[best_next_action]
        self.q_table[state][action] += self.config.learning_rate * (target_q - current_q)
        self.logger.debug(f"Updated Q[{state}, {action}] = {self.q_table[state][action]:.2f}")

    def save_state(self, filename: str = "agent_state.json"):
        # Save Q-table and epsilon to JSON
        state = {
            "q_table": [[list(k), v] for k, v in self.q_table.items()],
            "epsilon": self.epsilon
        }
        with open(filename, "w") as file:
            json.dump(state, file, indent=2)
        self.logger.info(f"Saved state to {filename}")

    def load_state(self, filename: str = "agent_state.json"):
        # Load Q-table and epsilon from JSON
        if not os.path.exists(filename):
            raise FileNotFoundError(f"State file {filename} not found")
        with open(filename, "r") as file:
            state = json.load(file)
        self.q_table = {tuple(k): v for k, v in state["q_table"]}
        self.epsilon = state["epsilon"]
        self.logger.info(f"Loaded state from {filename}")

    def prune_q_table(self, max_size: int = 100000):
        # Prune Q-table to max_size, keeping states with largest Q-values
        if len(self.q_table) > max_size:
            sorted_states = sorted(self.q_table.items(), key=lambda x: sum(abs(v) for v in x[1]))
            self.q_table = dict(sorted_states[-max_size:])
            self.logger.info(f"Pruned Q-table to {max_size} states")
