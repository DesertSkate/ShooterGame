import pygame
import time
from Entities.Player import player
from Entities.Enemies import Enemy, update_rects
from Entities.Map import map

pygame.init()
pygame.font.init()
size = width, height = 1200, 800
window = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("IR")

Map = map(window)
Map.gen_map()
test_tile = Map.get_empty_tile(True)
Player = player(window, "Player", "player", 12, (34, 199, 64), 3, 15, test_tile[0], test_tile[1], (25, 45))
projectiles = []
enemies = []
enemy_rects = []
playing = True
print(Map.map_array)

Map.generate_enemies(5, enemies)

while playing:
    window.fill((0, 0, 0))
    Map.draw_map()
    Map.draw_test_lines()
    enemy_rects = update_rects(enemies)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: playing = False

    if Player.check_death():
        playing = False
    Player.dash()
    if Map.smart_collide(Player, False) or Player.check_boundaries():
        Player.dashing = False
        Player.dash_time = time.time()
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
        # print(enemy.generate_path((Player.x,Player.y)))
        if enemy.check_death():
            enemies.remove(enemy)
            continue
        if enemy.ai[2] == "hunter-killer":
            pygame.draw.line(window, (0,0,255), (enemy.x,enemy.y), enemy.path_point)
        enemy.move()
        if Map.smart_collide(enemy, True) or enemy.check_boundaries():
            enemy.moving = False
            enemy.move_time = time.time()
        if enemy.has_LOS(Player, Map.rect_array): enemy.shoot(projectiles, Player)
        enemy.draw((Player.x,Player.y))

    if len(enemies) == 0 and len(Map.win_rects) == 0:
        Map.set_win()
    elif len(Map.win_rects) > 0 and Player.player_rect.collidelist(Map.win_rects) > -1:
        Map.gen_map()
        Map.generate_enemies(5, enemies)
        if Player.y <= 80:
            pos = Map.get_empty_tile(True, 9)
            Player.x, Player.y = pos
        else:
            pos = Map.get_empty_tile(True, 0)
            Player.x, Player.y = pos
            print(Map.get_empty_tile(pos))

    Player.draw()
    clock.tick(80)
    pygame.display.update()
    # print(enemies[0].path_point, enemies[0].x, enemies[0].y)
