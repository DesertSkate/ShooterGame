import pygame
import random
from Entities.Player import player
from Entities.Enemies import Enemy, update_rects

pygame.init()
size = width, height = 1200, 800
window = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Boom")

Player = player(window, "Player", "player", 12, (34, 199, 64), 3, 15, width/2, height/2, (25, 45))
projectiles = []
enemies = []
enemy_rects = []
playing = True

for x in range(10):
    pos = (random.randint(300, 800), random.randint(200, 400))
    new_enemy = Enemy(window, f"Enemy{x}", "enemy", 3, ("basic", "single"), (181,18,18), 2, 2, pos[0], pos[1], (30,30))
    enemies.append(new_enemy)

while playing:
    window.fill((0, 0, 0))
    enemy_rects = update_rects(enemies)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: playing = False

    Player.move()
    Player.shoot(projectiles)
    for projectile in projectiles:
        collide = projectile.proj.collidelist(enemy_rects)
        if projectile.check_boundary():
            projectiles.remove(projectile)
            continue
        if collide > -1:
            enemies[collide].take_damage(projectile.damage)
            projectiles.remove(projectile)
            continue
        projectile.update()

    for enemy in enemies:
        if enemy.check_death():
            enemies.remove(enemy)
            continue
        enemy.move()
        enemy.draw()

    Player.draw()
    clock.tick(60)
    pygame.display.update()
    # print(enemies[0].path_point, enemies[0].x, enemies[0].y)