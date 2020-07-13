import pygame
import time


class entity:
    def __init__(self, window, name, iff, health, color, speed=0, x=0, y=0, size=(0,0)):
        self.window = window
        self.name = name
        self.iff = iff
        self.health = health
        self.init_color = color
        self.color = color
        self.speed = speed
        self.x = x
        self.y = y
        self.size = size

        self.damage_time = time.time()

    def take_damage(self, damage):
        self.damage_time = time.time()
        self.color = (255, 255, 255)

        self.health -= damage

    def check_boundaries(self):
        width, height = pygame.display.get_surface().get_size()
        if self.x + self.size[0] > width:
            self.x = width - self.size[0]
        elif self.x < 0:
            self.x = 0
        if self.y - self.size[1] > height:
            self.y = height - self.size[0]
        elif self.y < 0:
            self.y = 0

    def check_death(self):
        if self.health <= 0:
            return True
        return False


class projectile:
    def __init__(self, window, x, y, x_speed, y_speed, radius, damage, color, iff):
        self.window = window
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.radius = radius
        self.damage = damage
        self.color = color
        self.iff = iff

        self.proj = pygame.draw.circle(self.window, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed

        self.proj = pygame.draw.circle(self.window, self.color, (int(self.x), int(self.y)), self.radius)

    def check_boundary(self):
        width, height = pygame.display.get_surface().get_size()
        if self.x > width or self.x < 0:
            return True
        if self.y > height or self.y < 0:
            return True