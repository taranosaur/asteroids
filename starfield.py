import pygame
import random

from constants import *


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, size):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)  # Transparent surface
        pygame.draw.circle(self.image, (255, 255, 255), (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Set initial position
        self.speed = speed
        self.size = size  # Save size for custom drawing

    def update(self, *args):
        dt = args[0] if args else 1
        self.rect.y += self.speed * dt
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        # Use rect attributes to position the star
        pygame.draw.circle(screen, (255, 255, 255), self.rect.center, self.size)


class Starfield:
    def __init__(self, num_stars):
        for _ in range(num_stars):
            star = Star(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.uniform(1, 4),  # Speed
                random.randint(1, 3)  # Size
            )
            self.add_star_to_containers(star)

    def add_star_to_containers(self, star):
        for container in Star.containers:
            container.add(star)

           

   
