import os
import time
from typing import Optional, Tuple, List
from config import GameConfig
from environment import GameEnvironment


class GameRenderer:
    def __init__(self, environment: GameEnvironment, config: GameConfig):
        # Initialize renderer with environment and config
        self.environment = environment
        self.config = config

    def render(self, state: Optional[Tuple[int, int, int]] = None, action: Optional[int] = None,
               reward: Optional[float] = None, status: Optional[str] = None, episode: Optional[int] = None,
               step: Optional[int] = None, epsilon: Optional[float] = None, q_values: Optional[List[float]] = None,
               enable: bool = True):
        # Render game state to console if enabled
        if not enable:
            return
        os.system("cls" if os.name == "nt" else "clear")
        for row in self.environment.grid:
            print("".join(row))
        print(f"Score: {self.environment.score}")
        print("-" * 40)
        if state is not None:
            distance, obstacle_type, agent_row = state
            print(f"State: Distance={distance} | Obstacle={obstacle_type} | Row={agent_row}")
        if action is not None and reward is not None:
            action_str = "JUMP" if action == 1 else "STAY"
            print(f"Action: {action_str} | Reward: {reward} | Status: {status}")
        if episode is not None and step is not None:
            print(f"Episode: {episode} | Step: {step} | Epsilon: {epsilon:.3f}")
        if q_values is not None:
            print(f"Q-values: [STAY={q_values[0]:.2f}, JUMP={q_values[1]:.2f}]")
            best_action = "STAY" if q_values[0] >= q_values[1] else "JUMP"
            print(f"Predicted Best Action: {best_action}")
        time.sleep(self.config.render_delay)
