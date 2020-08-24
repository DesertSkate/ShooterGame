import pygame
import time
import random
from .Entity import entity, projectile, Node

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
        print(self.path)
        if self.ai[2] == "hunter-killer" and len(self.path) > 0:
            self.path_point = (self.path[0][0] * 80 + 40, self.path[0][1] * 80 + 40)
            print(self.path_point)
            self.path.remove(self.path[0])
        x, y = self.path_point
        x2, y2 = x - self.x, y - self.y
        distance = (x2 ** 2 + y2 ** 2) ** .5

        if distance < 1 and self.ai != "hunter-killer":
            self.moving = False
            self.move_time = time.time()
            return
        elif distance < 1 and self.ai[2] == "hunter-killer" and len(self.path) == 0:
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
            if self.ai[2] == "hunter-killer":
                self.moving = True
                self.path = self.generate_path(player_pos)
        if not time.time() > self.damage_time + 2:
            self.draw_healthbar()
            print(self.damage_time)

        self.enemy_rect = pygame.Rect((self.x, self.y),
                                       self.size)
        pygame.draw.rect(self.window, self.color, self.enemy_rect)

    def get_adjacent(self, cur_index):  # Top, right, bottom, left
        adjacent = []
        if not cur_index[1] == 0:
            adjacent.append([cur_index[1] + 1, cur_index[0]])
        if cur_index[0] != len(self.map.map_array) - 1:
            adjacent.append([cur_index[1] - 1, cur_index[0]])
        if cur_index[1] != len(self.map.map_array) - 1:
            adjacent.append([cur_index[1] - 1, cur_index[0]])
        if not cur_index[0] == 0:
            adjacent.append([cur_index[1], cur_index[0] - 1])
        return adjacent

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

    def has_LOS(self, player_item, rect_list): # LOS = Line of Sight
        for i in rect_list:
            if i.clipline(self.x, self.y, player_item.x, player_item.y):
                return False
        return True

    def generate_path(self, end_point=()):
        start_node = Node(None, self.map.get_square_by_pos((self.x,self.y)))
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, self.map.get_square_by_pos(end_point))
        end_node.g = end_node.h = end_node.f = 0

        to_visit = [start_node]
        visited = []
        outer_iterations = 0
        max_iterations = 1000  # (len(self.map.map_array) // 2) ** 10

        while len(to_visit) > 0:
            outer_iterations += 1

            movements = [[1,0],[0,1],[-1,0],[0,-1]]

            current_node = to_visit[0]
            current_index = 0
            for index, item in enumerate(to_visit):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            if outer_iterations > max_iterations:
                print("Too many iterations")
                return []

            to_visit.pop(current_index)
            visited.append(current_node)
            if tuple(current_node.position) == tuple(end_node.position):
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                # print(path)
                return path[::-1]

            children = []

            for new_pos in movements:
                node_pos = (current_node.position[0] + new_pos[0], current_node.position[1] + new_pos[1])

                if (node_pos[0] > len(self.map.map_array[0]) - 1 or
                    node_pos[0] < 0 or
                    node_pos[1] > len(self.map.map_array) - 1 or
                    node_pos[1] < 0):
                    continue

                if self.map.map_array[node_pos[1]][node_pos[0]] != 0:
                    continue

                new_node = Node(current_node, node_pos)
                children.append(new_node)

            for child in children:
                if len([visited_child for visited_child in visited if visited_child == child]) > 0:
                    continue

                child.g = current_node.g + 1
                child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
                child.f = child.h + child.g

                if len([i for i in to_visit if child == i and child.g > i.g]) > 0:
                    continue

                to_visit.append(child)
        return []


def update_rects(enemy_list):
    list = []
    for enemy in enemy_list:
        list.append(enemy.enemy_rect)

    return list

def sort_f(e):
    return e.f
