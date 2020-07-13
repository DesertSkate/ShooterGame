import pygame
import time
import random
from .Entity import entity, projectile


class Enemy(entity):
    def __init__(self, window, name, iff, health, ai, color, bullet_speed=2, speed=0, x=0, y=0, size=(0,0)):
        self.ai = ai
        self.bullet_speed = bullet_speed
        self.moving = False
        self.path_point = (x, y)
        super().__init__(window, name, iff, health, color, speed, x, y, size)
        self.enemy_rect = pygame.Rect((self.x - self.size[0] / 2, self.y - self.size[1] / 2),
                                      self.size)

    def shoot(self):
        pass

    def get_point(self): # ai should be formatted as: (movement type/personality, weapon type)
        p_type = self.ai[0]
        # if self.moving:
        #     return
        # self.moving = True
        if p_type == "basic":
            self.path_point = (self.x + random.randint(-600, 600), self.y + random.randint(-400, 400))

    def move(self):
        pass

    def draw(self):
        super().check_boundaries()
        if time.time() > self.damage_time + 0.3:
            self.color = self.init_color

        self.enemy_rect = pygame.Rect((self.x - self.size[0] / 2, self.y - self.size[1] / 2),
                                       self.size)
        pygame.draw.rect(self.window, self.color, self.enemy_rect)

def update_rects(enemy_list):
    list = []
    for enemy in enemy_list:
        list.append(enemy.enemy_rect)

    return list
