from config import *
from units import Player, Goblin, Fireball
from unit_layer import UnitLayer

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

player = Player(0, 350)

unit_layer = UnitLayer()
goblin = Goblin(100, 350)

unit_layer.add(player)
unit_layer.add(goblin)
unit_layer.add(Goblin(230, 270))


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                unit_layer.add_non_collide(Fireball(player, goblin, 1))

    player_move_speed = int(120 / FPS)
    # goblin.move(1, 0)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        unit_layer.move(player, 0, -player_move_speed)
    if keys[pygame.K_a]:
        unit_layer.move(player, -player_move_speed, 0)
    if keys[pygame.K_s]:
        unit_layer.move(player, 0, player_move_speed)
    if keys[pygame.K_d]:
        unit_layer.move(player, player_move_speed, 0)

    screen.fill(BLUE)

    unit_layer.draw(screen)

    pygame.display.flip()

pygame.quit()
