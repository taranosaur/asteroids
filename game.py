import pygame
from states import State  # Ensure State is imported

class Game:
    def __init__(self, initial_state_class):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))  # Replace with SCREEN_WIDTH, SCREEN_HEIGHT
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = initial_state_class(self)

    def change_state(self, new_state):
        """Switch to a new state."""
        if isinstance(new_state, State):  # Check if it's already an instance
            self.current_state = new_state
        else:
            self.current_state = new_state(self)  # Instantiate the state class

    def run(self):
        """Main game loop."""
        while self.running:
            events = pygame.event.get()
            dt = self.clock.tick(60) / 1000

            self.current_state.handle_events(events)
            self.current_state.update(dt)
            self.current_state.render(self.screen)


