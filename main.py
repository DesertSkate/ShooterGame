import pygame
import random
from Entities.Player import player
from Entities.Enemies import Enemy, update_rects
from Entities.Map import map

pygame.init()
size = width, height = 1200, 800
window = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Boom")

Map = map(window)
Map.gen_map()
test_tile = Map.get_empty_tile(True)
Player = player(window, "Player", "player", 12, (34, 199, 64), 3, 15, test_tile[0], test_tile[1], (25, 45))
projectiles = []
enemies = []
enemy_rects = []
playing = True

for x in range(5):
    pos = Map.get_empty_tile(True)
    new_enemy = Enemy(window, f"Enemy{x}", "enemy", 3, ("basic", "single"), (181,18,18), 2, 2, pos[0], pos[1], (30,30))
    enemies.append(new_enemy)

while playing:
    window.fill((0, 0, 0))
    Map.draw_map()
    enemy_rects = update_rects(enemies)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: playing = False

    Player.dash()
    Player.move()
    Map.smart_collide(Player, True)
    Player.shoot(projectiles)
    for projectile in projectiles:
        collide = projectile.proj.collidelist(enemy_rects)
        collide2 = Player.player_rect.colliderect(projectile.proj)
        if projectile.check_boundary():
            projectiles.remove(projectile)
            continue
        if Map.smart_collide(projectile, False):
            projectiles.remove(projectile)
            continue
        if collide > -1 and projectile.iff != "enemy":
            enemies[collide].take_damage(projectile.damage)
            projectiles.remove(projectile)
            continue
        if collide2 and projectile.iff != "player" and not Player.dashing:
            Player.take_damage(projectile.damage)
            projectiles.remove(projectile)
            continue
        projectile.update()

    for enemy in enemies:
        if enemy.check_death():
            enemies.remove(enemy)
            continue
        enemy.move()
        Map.smart_collide(enemy, True)
        enemy.shoot(projectiles, (Player.x, Player.y))
        enemy.draw()

    Player.draw()
    # print(Player.x, Player.y)
    # print(Map.get_square_by_pos((Player.x, Player.y)))
    clock.tick(60)
    pygame.display.update()
    # print(enemies[0].path_point, enemies[0].x, enemies[0].y)