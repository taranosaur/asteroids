import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score_manager import ScoreManager
from starfield import Star, Starfield

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    score_manager = ScoreManager()


    Asteroid.containers = (asteroids, updateable, drawable)
    Player.containers = (updateable, drawable)
    AsteroidField.containers = (updateable)
    Shot.containers = (shots, updateable, drawable)
    Star.containers = (updateable, drawable)
    

    asteroid_field = AsteroidField(score_manager)
    starfield = Starfield(100)
    player = Player(SCREEN_WIDTH /2, SCREEN_HEIGHT /2, PLAYER_RADIUS)


    player_score = 0
    font = pygame.font.Font(pygame.font.get_default_font(), 24)

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updateable:
            obj.update(dt)
        
        for obj in asteroids:
            if player.collision(obj) == True:
                print("Game over!")
                return
        
        for asteroid in asteroids:
            for bullet in shots:
                if asteroid.collision(bullet) == True:
                    asteroid.split()
                    bullet.kill()

            
        screen.fill("black")
        
        for obj in drawable:
            obj.draw(screen)   
        
        score_text = font.render(f"Score: {score_manager.get_score()}", True, "white")
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        dt = clock.tick(60) / 1000

        
            


if __name__ == "__main__":
    main()