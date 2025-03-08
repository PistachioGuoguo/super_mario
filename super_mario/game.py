import os
import pygame
import sys
from typing import Tuple, List

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
FPS = 60
GRAVITY = 0.8
JUMP_SPEED = -15
MOVE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
BROWN = (139, 69, 19)

class Mario(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((255, 0, 0))  # Red color for Mario
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.on_ground = False

    def update(self, platforms: pygame.sprite.Group):
        # Gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_SPEED

class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Super Mario")
        self.clock = pygame.time.Clock()
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        
        # Create Mario
        self.mario = Mario(100, 300)
        self.all_sprites.add(self.mario)
        
        # Create ground
        ground = Platform(0, 550, 800, 50)
        self.all_sprites.add(ground)
        self.platforms.add(ground)
        
        # Create some platforms
        platform_positions = [
            (300, 400, 200, 20),
            (100, 300, 200, 20),
            (500, 200, 200, 20),
        ]
        
        for x, y, w, h in platform_positions:
            platform = Platform(x, y, w, h)
            self.all_sprites.add(platform)
            self.platforms.add(platform)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mario.jump()
        return True

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.mario.rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.mario.rect.x += MOVE_SPEED
            
        self.mario.update(self.platforms)

    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 