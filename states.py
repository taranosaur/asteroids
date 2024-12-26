import pygame
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score_manager import ScoreManager
from starfield import Starfield
from constants import *
from particles import Particle

# Base State Class
class State:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass


# Gameplay State
class GameplayState(State):
    def __init__(self, game):
        super().__init__(game)
        self.updateable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.explosions = []  # Store explosions
        self.particles = []

        # Set containers
        Asteroid.containers = (self.asteroids, self.updateable, self.drawable)
        Player.containers = (self.updateable, self.drawable)
        AsteroidField.containers = (self.updateable)
        Shot.containers = (self.shots, self.updateable, self.drawable)

        # Initialize game objects
        self.score_manager = ScoreManager()
        self.asteroid_field = AsteroidField(self.score_manager)
        self.starfield = Starfield(100, 3)
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False


    def update_particles(self, dt):
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.radius <= 0:  # Remove "dead" particles
                self.particles.remove(particle)


    def update(self, dt):
        # Update starfield
        self.starfield.update(dt)

        # Update all game objects
        for obj in self.updateable:
            obj.update(dt)

        # Update explosions
        self.update_explosions(dt)
        self.update_particles(dt)

        # Check for collisions
        for asteroid in self.asteroids:
            if self.player.collision(asteroid):
                self.game.change_state(GameOverState(self.game, self.score_manager.get_score()))
                return

        for asteroid in self.asteroids:
            for shot in self.shots:
                if asteroid.collision(shot):
                    asteroid.split(self.explosions, self.particles)  # Pass the explosions list
                    shot.kill()

    def render(self, screen):
        # Clear screen
        screen.fill("black")

        # Draw background starfield
        self.starfield.draw(screen)

        # Draw all drawable game objects
        for obj in self.drawable:
            obj.draw(screen)

        # Render explosions
        self.render_explosions(screen)
        self.render_particles(screen)

        # Display score
        score_text = self.font.render(f"Score: {self.score_manager.get_score()}", True, "white")
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

    def update_explosions(self, dt):
        """Update ongoing explosions."""
        for explosion in self.explosions[:]:
            explosion["elapsed_time"] += dt
            if explosion["elapsed_time"] >= explosion["duration"]:
                self.explosions.remove(explosion)  # Remove finished explosions
            else:
                explosion["radius"] = (
                    explosion["elapsed_time"] / explosion["duration"]
                ) * explosion["max_radius"]

    def render_explosions(self, screen):
        """Render all active explosions."""
        for explosion in self.explosions:
            alpha = int(255 * (1 - explosion["elapsed_time"] / explosion["duration"]))
            color = (255, 100, 0)  # Bright orange
            pygame.draw.circle(
                screen, color, (int(explosion["position"].x), int(explosion["position"].y)), int(explosion["radius"])
            )
    
    def render_particles(self, screen):
        """Render all active particles."""
        for particle in self.particles:
            particle.draw(screen)


# Game Over State
class GameOverState(State):
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score
        self.font = pygame.font.Font(pygame.font.get_default_font(), 48)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    self.game.change_state(GameplayState(self.game))
                elif event.key == pygame.K_q:  # Quit
                    self.game.running = False

    def render(self, screen):
        screen.fill("black")
        text = self.font.render("Game Over", True, (255, 0, 0))
        score_text = self.font.render(f"Score: {self.score}", True, "white")
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, "white")

        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 300))
        pygame.display.flip()
