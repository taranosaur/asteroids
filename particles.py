import pygame
import random
from pygame.math import Vector2

class Particle:
    def __init__(self, position, velocity, color, lifespan, radius):
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.color = color
        self.lifespan = lifespan
        self.radius = radius
        self.age = 0

    def update(self, dt):
        """Update the particle's position and lifespan."""
        self.position += self.velocity * dt
        self.age += dt
        if self.age > self.lifespan:
            self.radius = 0  # Indicate the particle is "dead"

    def draw(self, screen):
        """Render the particle."""
        if self.radius > 0:
            alpha = max(0, 255 - int((self.age / self.lifespan) * 255))  # Fade out
            color = (*self.color[:3], alpha)  # Add alpha channel for fading
            pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), int(self.radius))
