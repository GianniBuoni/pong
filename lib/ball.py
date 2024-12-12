# pyright: reportOptionalMemberAccess = false
from lib.constants import *
from random import choice, uniform

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites) -> None:
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites

        # image
        self.image = pygame.Surface(SIZE["ball"], pygame.SRCALPHA)
        circle_rad = SIZE["ball"][0] / 2
        pygame.draw.circle(
            self.image,
            COLORS["ball"],
            (circle_rad, circle_rad),
            circle_rad
        )

        # rect
        self.rect = self.image.get_frect(center = (
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        ))
        self.rect_old = self.rect.copy()

        # movement
        self.direction = pygame.Vector2(
            choice((-1, 1)),
            uniform(0.7, 0.8) * choice((-1, 1))
        )
        self.speed = SPEED["ball"]

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.paddle_collide("horizontal")
        self.rect.y += self.direction.y * self.speed * dt
        self.paddle_collide("vertical")

    def paddle_collide(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.rect.right >= sprite.rect.left and self.rect_old.right <= sprite.rect_old.left:
                        self.rect.right = sprite.rect.left
                        self.direction *= -1
                    if self.rect.left <= sprite.rect.right and self.rect_old.left >= sprite.rect_old.right:
                        self.rect.left = sprite.rect.right
                        self.direction *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.rect_old.bottom <= sprite.rect_old.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction *= -1
                    if self.rect.top <= sprite.rect.bottom and self.rect_old.top >= sprite.rect_old.bottom:
                        self.rect.top = self.rect.bottom
                        self.direction *= -1

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
        self.rect_old = self.rect.copy()
        self.move(dt)
        self.wall_collide()
