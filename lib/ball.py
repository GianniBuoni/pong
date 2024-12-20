# pyright: reportOptionalMemberAccess = false
from lib.constants import *
from random import choice, uniform

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, score) -> None:
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = score

        # image
        self.image = pygame.Surface(SIZE["ball"], pygame.SRCALPHA)
        circle_rad = SIZE["ball"][0] / 2
        pygame.draw.circle(
            self.image,
            COLORS["ball"],
            (circle_rad, circle_rad),
            circle_rad
        )

        # shadow
        self.shadow_surface = self.image.copy()
        circle_rad = SIZE["ball"][0] / 2
        pygame.draw.circle(
            self.shadow_surface,
            COLORS["ball shadow"],
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
        self.speed_modifier = 0

        # reset timer
        self.reset_delay = 500
        self.start_time = pygame.time.get_ticks()

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt * self.speed_modifier
        self.paddle_collide("horizontal")
        self.rect.y += self.direction.y * self.speed * dt * self.speed_modifier
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
                        self.direction.x *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.rect_old.bottom <= sprite.rect_old.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction *= -1
                    if self.rect.top <= sprite.rect.bottom and self.rect_old.top >= sprite.rect_old.bottom:
                        self.rect.top = self.rect.bottom
                        self.direction.y *= -1

    def wall_collide(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        if self.rect.left <= 0:
            self.update_score("player")
            self.reset()
        if self.rect.right >= WINDOW_WIDTH:
            self.update_score("opponent")
            self.reset()

    def reset(self):
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.direction = pygame.Vector2(
            choice((-1, 1)),
            uniform(0.7, 0.8) * choice((-1, 1))
        )
        self.start_time = pygame.time.get_ticks()

    def reset_timer(self):
        if pygame.time.get_ticks() - self.start_time >= self.reset_delay:
            self.speed_modifier = 1
        else: self.speed_modifier = 0

    def update(self, dt):
        self.rect_old = self.rect.copy()
        self.reset_timer()
        self.move(dt)
        self.wall_collide()
