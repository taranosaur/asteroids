import pygame
import random

from constants import *
from circleshape import CircleShape
from score_manager import ScoreManager






class Asteroid(CircleShape):
    def __init__(self, x, y, radius, score_manager):
        super().__init__(x, y, radius)
        self.score_manager = score_manager

    def draw(self, screen):
        pygame.draw.circle(screen, "white",self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
    
    def split (self):
        
        self.score_manager.increment(10)

        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            random_angle = random.uniform(20, 50)
            vector1 = self.velocity.rotate(random_angle)
            vector2 = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            asteroid_one = Asteroid(self.position.x, self.position.y, new_radius, self.score_manager)
            asteroid_two = Asteroid(self.position.x, self.position.y, new_radius, self.score_manager)

            asteroid_one.velocity = vector1 * 1.2
            asteroid_two.velocity = vector2 * 1.2