import pygame
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score_manager import ScoreManager
from starfield import Starfield
from constants import *

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

    def update(self, dt):
        self.starfield.update(dt)
        for obj in self.updateable:
            obj.update(dt)

        # Check for collisions
        for asteroid in self.asteroids:
            if self.player.collision(asteroid):
                self.game.change_state(GameOverState(self.game, self.score_manager.get_score()))
                return

        for asteroid in self.asteroids:
            for shot in self.shots:
                if asteroid.collision(shot):
                    asteroid.split()
                    shot.kill()

    def render(self, screen):
        screen.fill("black")
        self.starfield.draw(screen)
        for obj in self.drawable:
            obj.draw(screen)

        # Display score
        score_text = self.font.render(f"Score: {self.score_manager.get_score()}", True, "white")
        screen.blit(score_text, (10, 10))
        pygame.display.flip()


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
