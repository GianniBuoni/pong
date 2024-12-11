import pygame

from lib.constants import *

class Game():
    def __init__(self):
        # initialize
        pygame.init()
        self.running = True
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            # delta time
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            # draw
            self.display_surface.fill("black")
            pygame.display.update()
        pygame.quit()
