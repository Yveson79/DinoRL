from typing import Tuple, List, Dict
import random
from config import GameConfig, ObstacleType


class GameEnvironment:
    def __init__(self, config: GameConfig):
        # Initialize game environment with config
        self.config = config
        self.width = config.width
        self.height = config.height
        self.grid = [[config.empty_symbol for _ in range(self.width)] for _ in range(self.height)]
        self.agent_position = list(config.initial_agent_position)
        self.grid[self.agent_position[0]][self.agent_position[1]] = config.agent_symbol
        self.obstacles: List[Dict[str, int]] = []
        self.score = 0

    def reset(self) -> Tuple[int, int, int]:
        # Reset grid, agent position, obstacles, and score
        self.grid = [[self.config.empty_symbol for _ in range(self.width)] for _ in range(self.height)]
        self.agent_position = list(self.config.initial_agent_position)
        self.grid[self.agent_position[0]][self.agent_position[1]] = self.config.agent_symbol
        self.obstacles = []
        self.score = 0
        return self.get_state()

    def get_state(self) -> Tuple[int, int, int]:
        # Return current state: (distance to closest obstacle, obstacle type, agent row)
        if not self.obstacles:
            return (self.width, 0, self.agent_position[0])
        closest = min(self.obstacles, key=lambda o: o["col"])
        distance = closest["col"] - self.agent_position[1]
        distance = max(0, min(self.width, distance))
        obstacle_type = closest["type"]
        return (distance, obstacle_type, self.agent_position[0])

    def spawn_obstacle(self):
        # Spawn a new obstacle with 20% probability if below max_obstacles
        if len(self.obstacles) < self.config.max_obstacles and random.random() < 0.2:
            row = random.choice([0, 1])
            obstacle = {
                "row": row,
                "col": self.width - 1,
                "type": ObstacleType.TREE.value if row == 0 else ObstacleType.BIRD.value
            }
            self.obstacles.append(obstacle)
            symbol = self.config.tree_symbol if row == 0 else self.config.bird_symbol
            self.grid[row][self.width - 1] = symbol

    def move_obstacles(self):
        # Move all obstacles left and remove those off-screen
        for obstacle in self.obstacles[:]:
            row, col = obstacle["row"], obstacle["col"]
            self.grid[row][col] = self.config.empty_symbol
            col -= 1
            if col >= 0:
                obstacle["col"] = col
                symbol = self.config.bird_symbol if row == 1 else self.config.tree_symbol
                self.grid[row][col] = symbol
            else:
                self.obstacles.remove(obstacle)

    def step(self, action: int) -> Tuple[Tuple[int, int, int], float, bool]:
        # Execute one step: update agent, move/spawn obstacles, compute reward
        if action not in [0, 1]:
            raise ValueError(f"Invalid action: {action}")
        previous_position = self.agent_position.copy()
        self.agent_position[0] = 0 if action == 1 else 1
        self.grid[previous_position[0]][previous_position[1]] = self.config.empty_symbol
        self.grid[self.agent_position[0]][self.agent_position[1]] = self.config.agent_symbol
        self.move_obstacles()
        self.spawn_obstacle()
        reward = self.config.survival_reward
        done = False
        for obstacle in self.obstacles:
            if obstacle["col"] == self.agent_position[1]:
                if obstacle["row"] == self.agent_position[0]:
                    self.grid[self.agent_position[0]][self.agent_position[1]] = self.config.collision_symbol
                    reward = self.config.collision_reward
                    done = True
                else:
                    reward = self.config.dodge_reward
                    self.score += 1
        return self.get_state(), reward, done
