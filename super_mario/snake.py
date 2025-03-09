import random
import sys
from typing import Tuple

import pygame

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
GRID_SIZE = 20
GRID_WIDTH = WINDOW_SIZE[0] // GRID_SIZE
GRID_HEIGHT = WINDOW_SIZE[1] // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Start moving right
        self.grow_next = False

    def move(self) -> bool:
        head = self.body[0]
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT,
        )

        # Check for collision with self
        if new_head in self.body:
            return False

        self.body.insert(0, new_head)
        if not self.grow_next:
            self.body.pop()
        else:
            self.grow_next = False

        return True

    def grow(self):
        self.grow_next = True

    def change_direction(self, new_direction: Tuple[int, int]):
        # Prevent 180-degree turns
        if new_direction[0] != -self.direction[0] or new_direction[1] != -self.direction[1]:
            self.direction = new_direction


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = self.spawn_food()
        self.score = 0

    def spawn_food(self) -> Tuple[int, int]:
        while True:
            food = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if food not in self.snake.body:
                return food

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  # Up
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_s:  # Down
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_a:  # Left
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_d:  # Right
                    self.snake.change_direction((1, 0))
                elif event.key == pygame.K_r:  # Restart
                    self.reset_game()
        return True

    def update(self) -> bool:
        if not self.snake.move():
            return False

        # Check for food collision
        if self.snake.body[0] == self.food:
            self.snake.grow()
            self.food = self.spawn_food()
            self.score += 1

        return True

    def draw(self):
        self.screen.fill(BLACK)

        # Draw snake
        for i, segment in enumerate(self.snake.body):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(
                self.screen,
                color,
                (
                    segment[0] * GRID_SIZE,
                    segment[1] * GRID_SIZE,
                    GRID_SIZE - 1,
                    GRID_SIZE - 1,
                ),
            )

        # Draw food
        pygame.draw.rect(
            self.screen,
            RED,
            (
                self.food[0] * GRID_SIZE,
                self.food[1] * GRID_SIZE,
                GRID_SIZE - 1,
                GRID_SIZE - 1,
            ),
        )

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self):
        running = True
        game_over = False

        while running:
            running = self.handle_events()

            if not game_over:
                game_over = not self.update()

                if game_over:
                    game_over_text = self.font.render("Game Over! Press R to restart", True, WHITE)
                    text_rect = game_over_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
                    self.screen.blit(game_over_text, text_rect)
                    pygame.display.flip()

            self.draw()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
