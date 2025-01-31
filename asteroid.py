import pygame
import random

from constants import *
from circleshape import CircleShape
from score_manager import ScoreManager
from particles import Particle, Vector2






class Asteroid(CircleShape):
    def __init__(self, x, y, radius, score_manager):
        super().__init__(x, y, radius)
        self.score_manager = score_manager

    def draw(self, screen):
        pygame.draw.circle(screen, "white",self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
    
    def explode(self, explosions, particles):
        """Create an explosion effect at this asteroid's position."""
        explosion = {
            "position": self.position.copy(),
            "radius": self.radius * 0.5,
            "max_radius": self.radius,
            "duration": 0.4,
            "elapsed_time": 0,
        }
        explosions.append(explosion)

        for _ in range(20):  # Number of particles
            velocity = Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
            color = (255, random.randint(50, 150), 0)  # Bright orange/yellow colors
            lifespan = random.uniform(0.5, 1.0)  # Random lifespan
            radius = random.uniform(2, 4)  # Random particle size
            particles.append(Particle(self.position, velocity, color, lifespan, radius))

    def split (self, explosions, particles):
        
        self.score_manager.add_score(10)
        self.explode(explosions, particles)
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

            return [asteroid_one, asteroid_two]