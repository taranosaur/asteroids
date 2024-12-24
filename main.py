import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updateable, drawable)
    Player.containers = (updateable, drawable)
    AsteroidField.containers = (updateable)
    Shot.containers = (shots, updateable, drawable)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH /2, SCREEN_HEIGHT /2, PLAYER_RADIUS)

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
        
        
        pygame.display.flip()

        dt = clock.tick(60) / 1000

        
            


if __name__ == "__main__":
    main()