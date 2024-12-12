# pyright: reportOptionalMemberAccess = false
from lib.constants import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)

        # image
        self.image = pygame.Surface(SIZE["paddle"], pygame.SRCALPHA)
        pygame.draw.rect(
            self.image,
            COLORS["paddle"],
            pygame.FRect((0,0), SIZE["paddle"]),
            0, 4
        )

        # movement
        self.direction = 0 # paddle only moves on y axis
        self.speed = 0 # child should have an override

    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def get_diretion(self) -> None:
        raise NotImplemented("Child class get_diretion method not defined")

    def update(self, dt):
        self.rect_old = self.rect.copy()
        self.get_diretion()
        self.move(dt)

class Player(Paddle):
    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.rect = self.image.get_frect(center = POS["player"])
        self.rect_old = self.rect.copy()
        self.speed = SPEED["player"]

    def get_diretion(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

class Opponent(Paddle):
    def __init__(self, groups, ball_sprite) -> None:
        super().__init__(groups)
        self.rect = self.image.get_frect(center = POS["opponent"])
        self.rect_old = self.rect.copy()
        self.speed = SPEED["opponent"]
        self.ball = ball_sprite

    def get_diretion(self) -> None:
        self.direction = 1 if self.rect.centery < self.ball.rect.centery else -1
