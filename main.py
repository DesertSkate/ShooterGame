import pygame
from Entities.Player import player

pygame.init()
size = width, height = 1200, 800
window = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Boom")

Player = player(window, "Player", "player", 12, 3, 7, width/2, height/2, (25, 45))
projectiles = []
playing = True

while playing:
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: playing = False

    Player.move()
    Player.shoot(projectiles)
    for proj in projectiles:
        if proj.check_boundary():
            projectiles.remove(proj)
            continue
        proj.update()

    Player.draw()
    clock.tick(60)
    pygame.display.update()