import pygame
import time
from .Entity import entity, projectile


class player(entity):
    def __init__(self, window, name, iff, health, color, speed=0, bullet_speed=2, x=0, y=0, size=(0,0)):
        self.bullet_time = time.time()
        self.dash_time = time.time()
        self.dash_pos = (x, y)
        self.bullet_speed = bullet_speed
        self.dashing = False
        super().__init__(window, name, iff, health, color, speed, x, y, size)

        self.player_rect = pygame.Rect((self.x - self.size[0] / 2, self.y - self.size[1] / 2),
                                       self.size)

    def shoot(self, list): # https://stackoverflow.com/questions/52213088/how-to-shoot-a-bullet-at-an-angle-in-pygame
        cur_time = time.time()

        x, y = pygame.mouse.get_pos()[0] - self.size[0]/2, pygame.mouse.get_pos()[1] - self.size[1]/2
        x2, y2 = x - self.x, y - self.y
        distance = (x2 ** 2 + y2 ** 2) ** .5

        if distance != 0:
            normalized = self.bullet_speed
            multiplier = normalized / distance

            x2 *= multiplier * 0.5
            y2 *= multiplier * 0.5

        if pygame.mouse.get_pressed()[0]:
            if cur_time > self.bullet_time + 0.3:
                self.bullet_time = time.time()

                new_proj = projectile(self.window, int(self.x + self.size[0]/2), int(self.y + self.size[1]/2), x2, y2, 10, 1, (201, 113, 24), "player")
                list.append(new_proj)

    def move(self):
        if self.dashing:
            return
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: self.y -= self.speed
        elif keys[pygame.K_s]: self.y += self.speed
        if keys[pygame.K_a]: self.x -= self.speed
        elif keys[pygame.K_d]: self.x += self.speed

    def dash(self):
        dash_mod = 200
        if pygame.mouse.get_pressed()[2] and not self.dashing and time.time() > self.dash_time + 1:
            x, y = pygame.mouse.get_pos()
            if x > self.x + dash_mod:
                x = self.x + dash_mod
                print(1)
            elif x < self.x - dash_mod:
                x = self.x - dash_mod
                print(2)
            if y > self.y + dash_mod:
                y = self.y + dash_mod
                print(3)
            elif y < self.y - dash_mod:
                y = self.y - dash_mod
                print(4)
            self.dash_pos = (x, y)
            self.dashing = True
            return

        if self.dashing:
            x, y = self.dash_pos
            x2, y2 = x - self.x, y - self.y
            distance = (x2 ** 2 + y2 ** 2) ** .5

            if distance < self.size[0] / 5:
                self.dashing = False
                self.dash_time = time.time()
                return

            self.x += (x2 / distance) * self.speed * 3
            self.y += (y2 / distance) * self.speed * 3

    def draw(self):
        super().check_boundaries()
        if time.time() > self.damage_time + 0.3:
            self.color = self.init_color

        self.player_rect = pygame.Rect((self.x, self.y),
                                       self.size)
        pygame.draw.rect(self.window, self.color, self.player_rect)