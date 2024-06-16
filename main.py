import contextlib
from random import shuffle

from ability_choose_screen import AbilityChooseScreen
from background import Background
from camera import Camera
from config import *
from unit_generator import UnitGenerator
from unit_layer import UnitLayer
from upgrades_and_abilities.upgrades import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

camera = Camera()
background = Background(camera, screen)
unit_layer = UnitLayer(camera, screen)

goblin = unit_layer.create_goblin(100, 350)
unit_layer.create_goblin_archer(230, 270)
unit_generator = UnitGenerator(unit_layer)

running = True
pause = False
menu = None

upgrade_factory = UpgradeFactory(unit_layer.player)

start_lvl = 0

while running:
    clock.tick(FPS)
    background.draw()
    if start_lvl and not pause:
        pygame.event.post(pygame.event.Event(LVL_UP))
        start_lvl -= 1

    if not pause:
        unit_layer.process_next_frame()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ability_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
            with contextlib.suppress(ValueError, IndexError):
                ind = ability_keys.index(event.key)
                if ind != -1:
                    unit_layer.player.use_ability(ind)
        if event.type == LVL_UP:
            pause = True
            upgrade_list = upgrade_factory.get_all_upgrades()
            shuffle(upgrade_list)
            menu = AbilityChooseScreen(screen, upgrade_list[:3])
        if menu is not None:
            menu.handle_event(event)

    player_move_speed = int(120 / FPS)

    keys = pygame.key.get_pressed()
    if not pause:
        if keys[pygame.K_w]:
            unit_layer.move_player(0, -player_move_speed)
        if keys[pygame.K_a]:
            unit_layer.move_player(-player_move_speed, 0)
        if keys[pygame.K_s]:
            unit_layer.move_player(0, player_move_speed)
        if keys[pygame.K_d]:
            unit_layer.move_player(player_move_speed, 0)

        unit_layer.player.attack()
        unit_generator.step()

    unit_layer.draw()
    if menu is not None:
        res = menu.result
        if res is not None:
            res.upgrade(unit_layer.player)
            pause = False
            menu = None
        else:
            menu.draw()

    pygame.display.flip()
    logger.debug("----------------------")

pygame.quit()
