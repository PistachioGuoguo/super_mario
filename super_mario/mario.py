import sys

import pygame

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
FPS = 60
GRAVITY = 0.8
JUMP_SPEED = -15
MOVE_SPEED = 5
BULLET_SPEED = 10
BULLET_BOUNCE_DAMPING = 0.7  # Reduces bullet speed after bouncing

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = BULLET_SPEED * direction
        self.velocity_y = 0
        self.bounces = 0
        self.max_bounces = 5  # Maximum number of bounces before disappearing

    def update(self, platforms: pygame.sprite.Group):
        # Apply gravity
        self.velocity_y += GRAVITY * 0.5  # Reduced gravity effect on bullets

        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Check for collisions with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Vertical collision
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = -self.velocity_y * BULLET_BOUNCE_DAMPING
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = -self.velocity_y * BULLET_BOUNCE_DAMPING

                # Horizontal collision
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                    self.velocity_x = -self.velocity_x * BULLET_BOUNCE_DAMPING
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right
                    self.velocity_x = -self.velocity_x * BULLET_BOUNCE_DAMPING

                self.bounces += 1

        # Remove bullet if it's gone too far or bounced too many times
        if (
            self.rect.right < 0
            or self.rect.left > WINDOW_SIZE[0]
            or self.rect.bottom < 0
            or self.rect.top > WINDOW_SIZE[1]
            or self.bounces >= self.max_bounces
        ):
            self.kill()


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
        self.facing_right = True  # Track which direction Mario is facing

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

    def shoot(self) -> Bullet:
        direction = 1 if self.facing_right else -1
        return Bullet(self.rect.centerx + (20 * direction), self.rect.centery, direction)


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
        self.bullets = pygame.sprite.Group()

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
                if event.key == pygame.K_w:
                    self.mario.jump()
                elif event.key == pygame.K_SPACE:
                    bullet = self.mario.shoot()
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
        return True

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.mario.rect.x -= MOVE_SPEED
            self.mario.facing_right = False
        if keys[pygame.K_d]:
            self.mario.rect.x += MOVE_SPEED
            self.mario.facing_right = True

        self.mario.update(self.platforms)

        # Update bullets
        for bullet in self.bullets:
            bullet.update(self.platforms)

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
