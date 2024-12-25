import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white",self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

class Explosion(CircleShape):
    def __init__(self, x, y, max_radius, duration, color=(255, 100, 0)):
        super().__init__(x, y, 0, color)
        self.max_radius = max_radius
        self.duration = duration
        self.elapsed_time = 0

    def update(self, delta_time):
        """Update the explosion size and fade out."""
        self.elapsed_time += delta_time
        if self.elapsed_time < self.duration:
            self.radius = (self.elapsed_time / self.duration) * self.max_radius
        else:
            self.radius = 0  # Fully faded out