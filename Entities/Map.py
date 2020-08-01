import pygame
import random


class map:
    def __init__(self, window):
        self.window = window
        self.map_array = []
        self.rect_array = []  # consider removing and instead just using math and map array for collision

    def __init_map(self):
        window_size = pygame.display.get_surface().get_size()
        for i in range(int(window_size[1] / 80)):
            self.map_array.append([])
            for j in range(int(window_size[0] / 80)):
                self.map_array[i].append(0)
        print(self.map_array)

    def __gen_rects(self):
        for i in range(len(self.map_array)):
            for j in range(len(self.map_array[i])):
                if self.map_array[i][j] == 1:
                    new_rect = pygame.Rect((80 * j, 80 * i), (80,80))
                    self.rect_array.append(new_rect)

    def get_square_by_pos(self, pos):
        x, y = pos
        index = []
        for i in range(len(self.map_array[0])):
            if 80 * i <= x <= 80 * (i + 1):
                index.append(i)
                break
        for i in range(len(self.map_array)):
            if 80 * i <= y <= 80 * (i + 1):
                index.append(i)
                break

        return index

    def get_empty_tile(self, to_pos=False):
        index = random.randint(0, 9)
        tiles = []
        for i in range(len(self.map_array[index])):
            if self.map_array[index][i] == 0:
                tiles.append(i)
        if not to_pos:
            return [random.choice(tiles), index]
        else:
            return 80 * random.choice(tiles), 80 * index

    def gen_map(self):
        self.__init_map()
        for i in self.map_array:
            row_type = random.randint(1, 3)  # 1 = corridor, 2 = open, 3 = open with cover
            if row_type == 1:
                i[0:4] = [1] * 5
                i[10:] = [1] * 5
            elif row_type == 2:
                i[0:2] = [1] * 3
                i[12:] = [1] * 3
            elif row_type == 3:
                i[0:2] = [1] * 3
                i[6:8] = [1] * 3
                i[12:] = [1] * 3
        self.__gen_rects()

    def draw_map(self):
        for i in self.rect_array:
            pygame.draw.rect(self.window, (255,255,255), i)

    def draw_test_lines(self):
        window_size = pygame.display.get_surface().get_size()
        for i in range(len(self.map_array[0])):
            pygame.draw.line(self.window, (100, 100, 100), (0, 80 * i), (window_size[0], 80 * i), 2)
            pygame.draw.line(self.window, (100, 100, 100), (80 * i, 0), (80 * i, window_size[1]), 2)

    def smart_collide(self, item, fix=False):
        topL_index = self.get_square_by_pos((item.x, item.y))
        topR_index = self.get_square_by_pos((item.x + item.size[0], item.y))
        bottomL_index = self.get_square_by_pos((item.x, item.y + item.size[1]))
        bottomR_index = self.get_square_by_pos((item.x + item.size[0], item.y + item.size[1]))

        print(topL_index)
        print(bottomL_index)

        if self.map_array[topL_index[1]][topL_index[0]] == 1 and self.map_array[bottomL_index[1]][bottomL_index[0]] == 1:
            if fix: item.x = (80 * bottomL_index[0]) + 81

        if self.map_array[topR_index[1]][topR_index[0]] == 1 and self.map_array[bottomR_index[1]][bottomR_index[0]] == 1:
            if fix: item.x = (80 * bottomR_index[0]) - item.size[0]

        if self.map_array[topL_index[1]][topL_index[0]] == 1 and self.map_array[topR_index[1]][topR_index[0]] == 1:
            if fix: item.y = (80 * topL_index[1]) + 81

        if self.map_array[bottomL_index[1]][bottomL_index[0]] == 1 and self.map_array[bottomR_index[1]][bottomR_index[0]] == 1:
            if fix: item.y = (80 * bottomL_index[1]) - item.size[1]

        # if self.map_array[topL_index[1]][topL_index[0]] == 1 and self.map_array[bottomL_index[1]][bottomL_index[0]] == 0:
        #     if fix: item.y = (80 * topL_index[1]) + 81
