import pygame
import random

from constants import *


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, size):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed  # Fixed speed
        self.size = size

    def update(self, *args):
        dt = args[0] if args else 1
        print(f"Star updated: speed={self.speed}, dt={dt}")

        # Ensure speed remains constant by only using self.speed as set during initialization
        self.rect.y += self.speed * dt
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.uniform(-SCREEN_HEIGHT, 0)
            self.rect.x = random.randint(0, SCREEN_WIDTH)


    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.rect.center, self.size)



class Starfield:
    def __init__(self, num_stars, layers=3):
        self.layers = []
        distribution = [0.6, 0.3, 0.1]  # Adjust percentage per layer

        for layer in range(layers):
            stars_in_layer = int(num_stars * distribution[layer])  # Calculate stars for this layer
            base_speed = 30 + layer * 3  # Base speed increases with layer depth
            layer_stars = []

            for _ in range(stars_in_layer):
                star = Star(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT),  # Spread across full range
                    random.uniform(base_speed, base_speed + 2),
                    random.randint(1 + layer, 3 + layer)  # Adjust size per layer
                )
                layer_stars.append(star)

            self.layers.append(layer_stars)

    def update(self, dt):
        for layer in self.layers:
            for star in layer:
                star.update(dt)

    def draw(self, screen):
        for layer in self.layers:
            for star in layer:
                star.draw(screen)





           

   
