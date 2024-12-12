#pyright: reportOptionalMemberAccess = false
from os import mkdir, path
import json

from lib.constants import *
from lib.sprites import *

class Game():
    def __init__(self):
        # initialize
        pygame.init()
        self.running = True
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score)
        Opponent((self.all_sprites, self.paddle_sprites), self.ball)

        # scoring
        self.data_path = path.join("data", "score.json")
        if path.exists(self.data_path):
            with open(self.data_path) as f:
                self.score = json.load(f)
        else:
            self.score = { "player": 0, "opponent": 0 }
        self.font = pygame.font.Font(None, 160)

    def display_score(self):
        # player
        player_surface = self.font.render(str(self.score["player"]), True, COLORS["bg detail"])
        player_rect = player_surface.get_frect(center = (
            WINDOW_WIDTH / 2 + 100,
            WINDOW_HEIGHT / 2
        ))
        self.display_surface.blit(player_surface, player_rect)

        # opponent
        opponent_surface = self.font.render(str(self.score["opponent"]), True, COLORS["bg detail"])
        opponent_rect = opponent_surface.get_frect(center = (
            WINDOW_WIDTH / 2 - 100,
            WINDOW_HEIGHT / 2
        ))
        self.display_surface.blit(opponent_surface, opponent_rect)

        # line separation
        pygame.draw.line(
            self.display_surface, COLORS["bg detail"],
            (WINDOW_WIDTH / 2, 0),
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT),
            10
        )

    def update_score(self, paddle):
        self.score[paddle] += 1

    def run(self):
        while self.running:
            # delta time
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    data_dir = path.split(self.data_path)[0]
                    if not path.exists(data_dir):
                        mkdir(data_dir)
                    with open(self.data_path, "w") as f:
                        json.dump(self.score, f)

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(COLORS["bg"])
            self.display_score()
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        pygame.quit()
