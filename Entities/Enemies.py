import pygame
import time
import random
from .Entity import entity, projectile


class Enemy(entity):
    def __init__(self, window, name, iff, health, ai, color, bullet_speed=2, speed=0, x=0, y=0, size=(0,0)):
        self.ai = ai
        self.origin = (x, y)
        self.bullet_speed = bullet_speed
        self.moving = False
        self.move_time = time.time()
        self.shoot_time = time.time()
        self.path_point = (x, y)
        super().__init__(window, name, iff, health, color, speed, x, y, size)
        self.enemy_rect = pygame.Rect((self.x - self.size[0] / 2, self.y - self.size[1] / 2),
                                      self.size)

    def shoot(self, list, player_item):
        if not time.time() > self.shoot_time + self.get_idle_shoot():
            return

        x, y = player_item.x + player_item.size[0]/2, player_item.y + player_item.size[1]/2
        x2, y2 = x - self.x, y - self.y
        distance = (x2 ** 2 + y2 ** 2) ** .5

        if distance != 0:
            normalized = self.bullet_speed
            multiplier = normalized / distance

            x2 *= multiplier
            y2 *= multiplier

        self.shoot_time = time.time()
        new_proj = projectile(self.window, int(self.x + self.size[0]/2), int(self.y + self.size[1]/2), x2, y2, 10, 1, self.init_color,
                                          "enemy")
        list.append(new_proj)

    def move(self):
        if not self.moving:
            return
        x, y = self.path_point
        x2, y2 = x - self.x, y - self.y
        distance = (x2 ** 2 + y2 ** 2) ** .5

        if distance < 1:
            self.moving = False
            self.move_time = time.time()
            return

        self.x += (x2 / distance) * self.speed
        self.y += (y2 / distance) * self.speed

    def draw(self):
        super().check_boundaries()
        if time.time() > self.damage_time + 0.3:
            self.color = self.init_color
            self.damage_time = time.time()
        if time.time() > self.move_time + self.get_idle_time() and not self.moving:
            self.get_point()

        self.enemy_rect = pygame.Rect((self.x, self.y),
                                       self.size)
        pygame.draw.rect(self.window, self.color, self.enemy_rect)

    def get_point(self):  # ai should be formatted as: (movement type/personality, weapon type)
        p_type = self.ai[0]
        x, y = self.origin
        # if self.moving:
        #     return
        self.moving = True
        if p_type == "basic" or p_type == "fast-footed":
            self.path_point = (x + random.randint(-300, 300), y + random.randint(-200, 200))

    def get_idle_time(self):
        p_type = self.ai[0]
        if p_type == "basic":
            return 1
        elif p_type == "fast-footed":
            return 0.2

    def get_idle_shoot(self):
        total = 0
        p_type = self.ai[0]
        w_type = self.ai[1]
        if p_type == "basic" or p_type == "fast-footed":
            total += 1
        if w_type == "single":
            total += 0.5
        elif w_type == "quick-finger":
            total += 0.2
        return total

    def has_LOS(self, player_item, rect_list): # LOS = Line of Sight
        for i in rect_list:
            if i.clipline(self.x, self.y, player_item.x, player_item.y):
                return False
        return True


def update_rects(enemy_list):
    list = []
    for enemy in enemy_list:
        list.append(enemy.enemy_rect)

    return list
