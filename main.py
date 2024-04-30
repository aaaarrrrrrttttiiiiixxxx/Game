from config import *
from units import Player, Goblin, Fireball
from unit_layer import UnitLayer

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

player = Player()

unit_layer = UnitLayer()
goblin = Goblin(200, 350)

unit_layer.add(player)
unit_layer.add(goblin)
unit_layer.add(Goblin(230, 270))
unit_layer.add_non_collide(Fireball(player, goblin, 10))

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                player.move(0, -10)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        unit_layer.move(player, 0, -10)
    if keys[pygame.K_a]:
        unit_layer.move(player, -10, 0)
    if keys[pygame.K_s]:
        unit_layer.move(player, 0, 10)
    if keys[pygame.K_d]:
        unit_layer.move(player, 10, 0)

    screen.fill(BLUE)

    unit_layer.draw(screen)

    pygame.display.flip()

pygame.quit()
