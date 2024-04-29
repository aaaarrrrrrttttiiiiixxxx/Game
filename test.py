import pygame
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
player_rect = Rect(200, 500, 50, 50)
player_rect2 = Rect(220, 0, 50, 50)
gravity = 4
run = True

while run:
    clock.tick(60)
    player_rect2.bottom += gravity

    collide = pygame.Rect.colliderect(player_rect, player_rect2)

    if collide:
        player_rect2.bottom = player_rect.top

    pygame.draw.rect(window, (0, 255, 0), player_rect)
    pygame.draw.rect(window, (0, 0, 255), player_rect2)

    pygame.display.update()

    window.fill((255, 255, 255))
