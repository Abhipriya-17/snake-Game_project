# This is a classic Snake game built using the Pygame library.
# To run this code, you'll need to have Pygame installed.
# You can install it by running: pip install pygame

import pygame
import random
import sys

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# --- Directions ---
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Classes ---

class Snake:
    """Represents the snake player."""
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.growth_pending = False

    def move(self):
        """Moves the snake one step in its current direction."""
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check for growth before adding the new head
        if not self.growth_pending:
            self.body.pop()
        else:
            self.growth_pending = False
            
        self.body.insert(0, new_head)

    def change_direction(self, new_direction):
        """Changes the snake's direction, preventing reverse movement."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def grow(self):
        """Signals that the snake should grow on the next move."""
        self.growth_pending = True

    def get_head_position(self):
        """Returns the current position of the snake's head."""
        return self.body[0]

    def draw(self, surface):
        """Draws the snake on the game surface."""
        for segment in self.body:
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, BLACK, rect, 1) # border

class Food:
    """Represents the food for the snake."""
    def __init__(self):
        self.position = self.spawn_food()

    def spawn_food(self):
        """Generates a new random position for the food."""
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)

    def draw(self, surface):
        """Draws the food on the game surface."""
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1) # border

class Game:
    """Manages the main game loop and game state."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Python Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        """Resets the game to its initial state."""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def _handle_events(self):
        """Handles all Pygame events, including keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(RIGHT)

    def _check_collisions(self):
        """Checks for collisions with the food, walls, or the snake's own body."""
        head_pos = self.snake.get_head_position()

        # Collision with food
        if head_pos == self.food.position:
            self.snake.grow()
            self.score += 10
            self.food.position = self.food.spawn_food()

        # Collision with walls
        if (head_pos[0] < 0 or head_pos[0] >= GRID_WIDTH or
            head_pos[1] < 0 or head_pos[1] >= GRID_HEIGHT):
            self.game_over = True

        # Collision with self
        if head_pos in self.snake.body[1:]:
            self.game_over = True
            
    def _draw_elements(self):
        """Draws all game elements on the screen."""
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self._draw_score()
        
    def _draw_score(self):
        """Draws the current score on the screen."""
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (5, 5))

    def _display_game_over(self):
        """Displays the game over message and final score."""
        game_over_text = self.font.render("Game Over!", True, WHITE)
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        
        text_rect_go = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        text_rect_score = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        
        self.screen.blit(game_over_text, text_rect_go)
        self.screen.blit(final_score_text, text_rect_score)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.reset_game()
                    waiting = False

    def run(self):
        """The main game loop."""
        while True:
            self._handle_events()
            
            if not self.game_over:
                self.snake.move()
                self._check_collisions()
                self._draw_elements()
            else:
                self._display_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)

# --- Main execution block ---
if __name__ == "__main__":
    game = Game()
    game.run()
