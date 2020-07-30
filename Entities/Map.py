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
