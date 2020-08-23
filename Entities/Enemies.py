import pygame
import time
import random
from .Entity import entity, projectile

pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 20)


class Enemy(entity):
    def __init__(self, window, name, iff, health, ai, color, map_object, bullet_speed=2, speed=0, x=0, y=0, size=(0,0)):
        self.ai = ai
        self.map = map_object
        self.origin = (x, y)
        self.bullet_speed = bullet_speed
        self.moving = False
        self.move_time = time.time()
        self.shoot_time = time.time()
        self.path_point = (x, y)
        self.path = []
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

    def draw(self, player_pos):
        super().check_boundaries()
        if time.time() > self.damage_time + 0.3:
            self.color = self.init_color
        if time.time() > self.move_time + self.get_idle_time() and not self.moving:
            if self.ai[2] == "wander-origin":
                self.get_point()
        if not time.time() > self.damage_time + 2:
            self.draw_healthbar()
            print(self.damage_time)

        self.enemy_rect = pygame.Rect((self.x, self.y),
                                       self.size)
        pygame.draw.rect(self.window, self.color, self.enemy_rect)

    def get_open_directions(self, cur_index):  # Top, right, bottom, left
        return [self.map.map_array[cur_index[1] + 1][cur_index[0]] == 0, self.map.map_array[cur_index[1]][cur_index[0] + 1] == 0,
                self.map.map_array[cur_index[1] - 1][cur_index[0]] == 0, self.map.map_array[cur_index[1]][cur_index[0] - 1] == 0]

    def get_point(self):  # ai should be formatted as: (movement type/personality, weapon type, pathing type)
        p_type = self.ai[0]
        x, y = self.origin
        # if self.moving:
        #     return
        self.moving = True
        if p_type == "basic" or p_type == "fast-footed" or p_type == "quick-finger":
            self.path_point = (x + random.randint(-300, 300), y + random.randint(-200, 200))

    def get_idle_time(self):
        p_type = self.ai[0]
        if p_type == "basic" or p_type == "quick-finger":
            return 1
        elif p_type == "fast-footed":
            return 0.2

    def get_idle_shoot(self):
        total = 0
        p_type = self.ai[0]
        w_type = self.ai[1]
        if p_type == "basic" or p_type == "fast-footed":
            total += 1
        elif p_type == "quick-finger":
            total += 0.7
        if w_type == "single":
            total += 0.5
        elif w_type == "machine gun":
            total = 0.2
        return total

    def __get_tile_value(self, cur, e_index):
        base_value = cur[0] - e_index[0] if cur[0] >= e_index[0] else e_index[0] - cur[0]
        base_value += cur[1] - e_index[1] if cur[1] >= e_index[1] else e_index[1] - cur[1]
        # dirs = self.get_open_directions(cur)
        #
        # if dirs[0]
        #
        # value = values[0]
        return base_value

    def __get_path(self, cur_index, e_index):
        direction_index = []  # top, left, bottom, right
        direction_index.append([cur_index[0], cur_index[1] - 1] if cur_index[1] > 0 else False)
        direction_index.append([cur_index[0] - 1, cur_index[1]] if cur_index[0] > 0 else False)
        direction_index.append([cur_index[0], cur_index[1] + 1] if cur_index[1] + 1 < len(self.map.map_array) else False)
        direction_index.append([cur_index[0] + 1, cur_index[1]] if cur_index[0] + 1 < len(self.map.map_array[0]) else False)
        lowest = [1000, 0]

        print(direction_index)
        for x in direction_index:
            if not x:
                direction_index.remove(x)
                continue
            elif self.map.map_array[x[1]][x[0]] == 1:
                direction_index.remove(x)
                continue
        for x in direction_index:
            value = self.__get_tile_value(x, e_index)
            self.draw_tile_values((e_index[0] * 80, e_index[1] * 80), [value, x])

            x.append(value)

            if value == 0:
                lowest = [value, direction_index.index(x)]
                break
            elif value < lowest[0]:
                lowest = [value, direction_index.index(x)]

        return [direction_index[lowest[1]][0], direction_index[lowest[1]][1]]

    def has_LOS(self, player_item, rect_list): # LOS = Line of Sight
        for i in rect_list:
            if i.clipline(self.x, self.y, player_item.x, player_item.y):
                return False
        return True

    def generate_path(self, end_point):
        s_index = self.map.get_square_by_pos((self.x, self.y))
        e_index = self.map.get_square_by_pos(end_point)
        cur_index = s_index
        path = []
        looped = 0

        while looped < 100:  # replace with while
            looped += 1

            cur_index = self.__get_path(cur_index, e_index)
            if len(path) == 0 or cur_index != path[len(path) - 1]:
                path.append(cur_index)
            print(path)
            print(cur_index == e_index)
            if cur_index == e_index:
                break
        return path

    def draw_tile_values(self, end_point, val=False):
        e_index = self.map.get_square_by_pos(end_point)
        if not val == False:
            f_surface = font.render(str(val[0]), True, (255, 255, 255))
            self.window.blit(f_surface, (80 * val[1][0], 80 * val[1][1]))
            return
        for i in range(len(self.map.map_array)):
            for j in range(len(self.map.map_array[i])):
                print(self.map.map_array[i][j])
                if self.map.map_array[i][j] == 0:
                    cur_index = self.map.get_square_by_pos((80 * j, 80 * i))
                    val = self.__get_tile_value(cur_index, e_index)
                    f_surface = font.render(str(val), True, (255,255,255))
                    self.window.blit(f_surface, (80 * j, 80 * i))



def update_rects(enemy_list):
    list = []
    for enemy in enemy_list:
        list.append(enemy.enemy_rect)

    return list
