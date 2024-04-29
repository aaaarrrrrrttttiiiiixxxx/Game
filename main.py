import pygame

from constants import *
from player import Player

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

player = Player()

# Цикл игры
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.move(0, -10)
            if event.key == pygame.K_a:
                player.move(-10, 0)
            if event.key == pygame.K_s:
                player.move(0, 10)
            if event.key == pygame.K_d:
                player.move(10, 0)

    screen.fill(BLUE)
    pygame.draw.circle(screen, RED, (250, 250), 75)
    player.draw(screen)
    pygame.display.flip()

pygame.quit()
