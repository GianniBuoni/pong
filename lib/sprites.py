# pyright: reportOptionalMemberAccess = false
import pygame

from lib.constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)

        # images
        self.image = pygame.Surface(SIZE["paddle"])
        self.image.fill(COLORS["paddle"])
        self.rect = self.image.get_frect(center = POS["player"])

        # movement
        self.direction = 0 # paddle only moves on y axis
        self.speed = SPEED["player"]

    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def get_diretion(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

    def update(self, dt):
        self.get_diretion()
        self.move(dt)
