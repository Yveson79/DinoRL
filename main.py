import signal
import sys
import logging
from typing import Optional
from environment import GameEnvironment
from agent import QLearningAgent
from renderer import GameRenderer
from config import GameConfig, Action
from tqdm import tqdm


class GameError(Exception):
    # Custom exception for game-specific errors
    pass


stop_flag = False


def signal_handler(sig, frame):
    # Handle interrupt signals (Ctrl+C, Ctrl+Z)
    global stop_flag
    stop_flag = True
    logging.info("Interrupt signal received. Shutting down gracefully...")


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)


def setup_logging(log_file: str = "game.log"):
    # Configure logging to file and console
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


def display_menu():
    # Display interactive menu and return user choice
    print("\n=== Q-Learning Game Menu ===")
    print("1. Train Agent")
    print("2. Test Agent")
    print("3. Save Agent State")
    print("4. Load Agent State")
    print("5. Save Configuration")
    print("6. Exit")
    return input("Select an option (1-6): ")


def run_episode(agent: QLearningAgent, renderer: GameRenderer, explore: bool, episode: int, max_steps: int) -> float:
    # Run a single episode, optionally exploring
    global stop_flag
    state = agent.environment.reset()
    total_reward = 0
    for step in range(max_steps):
        if stop_flag:
            break
        action = agent.choose_action(state, explore)
        next_state, reward, done = agent.environment.step(action)
        if explore:
            agent.update_q_table(state, action, reward, next_state)
        status = ("COLLISION" if reward == agent.config.collision_reward else
                  "DODGE" if reward == agent.config.dodge_reward else
                  "SURVIVED")
        renderer.render(
            state=state,
            action=action,
            reward=reward,
            status=status,
            episode=episode,
            step=step,
            epsilon=agent.epsilon,
            q_values=agent.get_q_values(state)
        )
        total_reward += reward
        state = next_state
        if done:
            break
    return total_reward


def train_agent(agent: QLearningAgent, renderer: GameRenderer, episodes: int):
    # Train agent for specified episodes with progress bar
    global stop_flag
    for episode in tqdm(range(episodes), desc="Training"):
        if stop_flag:
            break
        total_reward = run_episode(agent, renderer, explore=True, episode=episode, max_steps=agent.config.max_steps)
        agent.epsilon = max(agent.config.min_epsilon, agent.epsilon * agent.config.epsilon_decay)
        agent.prune_q_table()
        if episode % 100 == 0:
            logging.info(f"Episode {episode}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.3f}")


def test_agent(agent: QLearningAgent, renderer: GameRenderer, episodes: int = 1):
    # Test agent for specified episodes, reporting average reward
    global stop_flag
    total_rewards = []
    for episode in tqdm(range(episodes), desc="Testing"):
        if stop_flag:
            break
        total_reward = run_episode(agent, renderer, explore=False, episode=episode, max_steps=agent.config.max_steps)
        total_rewards.append(total_reward)
    if total_rewards:
        avg_reward = sum(total_rewards) / len(total_rewards)
        logging.info(f"Test completed. Average Reward: {avg_reward:.2f}, Episodes: {len(total_rewards)}")


def main():
    # Main program loop with menu interaction
    setup_logging()
    config = GameConfig()
    environment = GameEnvironment(config)
    agent = QLearningAgent(environment, config)
    renderer = GameRenderer(environment, config)
    global stop_flag
    while not stop_flag:
        try:
            choice = display_menu()
            if choice == "1":
                episodes = input("Enter number of episodes to train (default: 1000): ") or str(config.episodes)
                episodes = int(episodes)
                if episodes <= 0:
                    raise ValueError("Episodes must be positive")
                train_agent(agent, renderer, episodes)
            elif choice == "2":
                episodes = input("Enter number of test episodes (default: 1): ") or "1"
                episodes = int(episodes)
                if episodes <= 0:
                    raise ValueError("Episodes must be positive")
                test_agent(agent, renderer, episodes)
            elif choice == "3":
                filename = input("Enter filename to save state (default: agent_state.json): ") or "agent_state.json"
                agent.save_state(filename)
                print(f"Agent state saved to {filename}")
            elif choice == "4":
                filename = input("Enter filename to load state (default: agent_state.json): ") or "agent_state.json"
                agent.load_state(filename)
                print(f"Agent state loaded from {filename}")
            elif choice == "5":
                filename = input("Enter filename to save config (default: game_config.json): ") or "game_config.json"
                config.save(filename)
                print(f"Configuration saved to {filename}")
            elif choice == "6":
                print("Exiting program.")
                break
            else:
                print("Invalid option. Please select 1-6.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except FileNotFoundError as e:
            print(f"File error: {e}")
        except GameError as e:
            print(f"Game error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            logging.error(f"Unexpected error: {e}", exc_info=True)
    print("Program terminated.")


if __name__ == "__main__":
    main()
