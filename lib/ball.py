# pyright: reportOptionalMemberAccess = false
from lib.constants import *
from random import choice, uniform

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_group) -> None:
        super().__init__(groups)

        # image
        self.image = pygame.Surface(SIZE["ball"], pygame.SRCALPHA)
        circle_rad = SIZE["ball"][0] / 2
        pygame.draw.circle(
            self.image,
            COLORS["ball"],
            (circle_rad, circle_rad),
            circle_rad
        )
        self.rect = self.image.get_frect(center = (
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        ))

        # movement
        self.direction = pygame.Vector2(
            choice((-1, 1)),
            uniform(0.7, 0.8) * choice((-1, 1))
        )
        self.speed = SPEED["ball"]

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def wall_collide(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction.x *= -1
        if self.rect.left >= WINDOW_WIDTH:
            self.rect.left = WINDOW_WIDTH
            self.direction.x *= -1

    def update(self, dt):
        self.move(dt)
        self.wall_collide()
