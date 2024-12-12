# pyright: reportOptionalMemberAccess = false
from lib.constants import *

class Player(pygame.sprite.Sprite):
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
        self.rect = self.image.get_frect(center = POS["player"])
        self.rect_old = self.rect.copy()

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
        self.rect_old = self.rect.copy()
        self.get_diretion()
        self.move(dt)
