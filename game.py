import contextlib
from random import shuffle

from ability_choose_screen import AbilityChooseScreen
from background import Background
from camera import Camera
from clock import Clock
from config import *
from unit_generator import UnitGenerator
from unit_layer import UnitLayer
from units.enemies import BigGoblin
from units.player import PlayerDeadException
from upgrades_and_abilities.upgrades import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = Clock()
        self.clock.reset()

        camera = Camera()
        self.background = Background(camera, self.screen)
        self.unit_layer = UnitLayer(camera, self.screen)

        self.goblin = self.unit_layer.create_goblin(100, 350)
        self.unit_layer.create_goblin_archer(230, 270)
        # self.unit_layer.create_enemy(BigGoblin, 230, 270)
        self.unit_generator = UnitGenerator(self.unit_layer)

        self.running = True
        self.pause = False
        self.menu = None

        self.upgrade_factory = UpgradeFactory(self.unit_layer.player)

        self.start_lvl = 0

    def run(self) -> int:  # type: ignore
        while self.running:
            self.clock.tick(FPS)
            self.background.draw()
            if self.start_lvl and not self.pause:
                pygame.event.post(pygame.event.Event(LVL_UP))
                self.start_lvl -= 1

            try:
                if not self.pause:
                    self.unit_layer.process_next_frame()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        ability_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
                        with contextlib.suppress(ValueError, IndexError):
                            ind = ability_keys.index(event.key)
                            if ind != -1:
                                self.unit_layer.player.use_ability(ind)
                    if event.type == LVL_UP:
                        self.pause = True
                        upgrade_list = self.upgrade_factory.get_all_upgrades()
                        shuffle(upgrade_list)
                        self.menu = AbilityChooseScreen(self.screen, upgrade_list[:3])
                    if self.menu is not None:
                        self.menu.handle_event(event)

                player_move_speed = int(120 / FPS)  # todo

                keys = pygame.key.get_pressed()
                if not self.pause:
                    if keys[pygame.K_w]:
                        self.unit_layer.move_player(0, -player_move_speed)
                    if keys[pygame.K_a]:
                        self.unit_layer.move_player(-player_move_speed, 0)
                    if keys[pygame.K_s]:
                        self.unit_layer.move_player(0, player_move_speed)
                    if keys[pygame.K_d]:
                        self.unit_layer.move_player(player_move_speed, 0)

                    self.unit_layer.player.attack()
                    self.unit_generator.step()
            except PlayerDeadException:
                pygame.display.quit()
                return self.unit_layer.player.level

            self.unit_layer.draw()
            if self.menu is not None:
                res = self.menu.result
                if res is not None:
                    res.upgrade(self.unit_layer.player)
                    self.pause = False
                    self.menu = None
                else:
                    self.menu.draw()

            pygame.display.flip()
            logger.debug("----------------------")
