from config import *
from unit_layer import UnitLayer
from units import Fireball

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

unit_layer = UnitLayer(screen)

player = unit_layer.create_player()
goblin = unit_layer.create_goblin(100, 350)
unit_layer.create_goblin_archer(230, 270)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2]:
                fireball = Fireball(unit_layer, screen, player.rect.center[0], player.rect.center[1], 1)
                fireball.set_target(unit_layer.get_nearest_mob(*pygame.mouse.get_pos()))
                unit_layer.add_non_collide(fireball)
            if event.key in [pygame.K_3, pygame.K_4]:
                fireball = Fireball(unit_layer, screen, player.rect.center[0], player.rect.center[1], 1)
                fireball.set_target(unit_layer.get_nearest_mob(*player.rect.center))
                unit_layer.add_non_collide(fireball)

    player_move_speed = int(120 / FPS)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        unit_layer.move_player(0, -player_move_speed)
    if keys[pygame.K_a]:
        unit_layer.move_player(-player_move_speed, 0)
    if keys[pygame.K_s]:
        unit_layer.move_player(0, player_move_speed)
    if keys[pygame.K_d]:
        unit_layer.move_player(player_move_speed, 0)

    screen.fill(BLUE)

    unit_layer.draw()

    pygame.display.flip()

pygame.quit()
