from upgrades import *
from ability_choose_screen import AbilityChooseScreen
from config import *
from unit_generator import UnitGenerator
from unit_layer import UnitLayer

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

unit_layer = UnitLayer(screen)

player = unit_layer.create_player()
goblin = unit_layer.create_goblin(100, 350)
unit_layer.create_goblin_archer(230, 270)
unit_generator = UnitGenerator(unit_layer)

running = True
pause = False
menu = None

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_F9, ]:
                pause = not pause
        if event.type == LVL_UP:
            pause = True
            menu = AbilityChooseScreen(screen, [HPUpgrade(), HPRagenUpgrade(), DamageUpgrade()])
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

        player.attack()
        unit_generator.step()
        unit_layer.process_next_frame()



    screen.fill(BLUE)
    unit_layer.draw()
    if menu is not None:
        res = menu.result
        if res is not None:
            res.upgrade(player)
            pause = False
            menu = None
        else:
            menu.draw()

    pygame.display.flip()

pygame.quit()
