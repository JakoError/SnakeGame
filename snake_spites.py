import random

import pygame

import objects as obj

BACKGROUND_FILE = "./game_image2/background.png"
BLOCK_FILE = "./game_image2/block.png"
LEADER_BLOCK_FILE = "game_image2/leader.png"
POINT_BLOCK_FILE = "game_image2/point.png"

SCREEN_RECT = pygame.Rect(0, 0, 803, 851)
BLOCK_RECT = pygame.Rect(0, 0, 25, 25)
FRAME_PER_SEC = 120

MAP_X = obj.Data.x
MAP_Y = obj.Data.y

M_UP = 1
M_RIGHT = 2
M_DOWN = 3
M_LEFT = 4
M_STOP = 0

MOVE_EVENT = pygame.USEREVENT

s_data = obj.Data()


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(BACKGROUND_FILE)
        self.rect = self.image.get_rect()


class BlockSpite(pygame.sprite.Sprite):

    def __init__(self, x, y, image=BLOCK_FILE):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * BLOCK_RECT.width
        self.rect.y = y * BLOCK_RECT.height

    def update(self):
        if not s_data.point:
            s_data.s_map[self.x][self.y] -= 1
            if s_data.s_map[self.x][self.y] == 0:
                self.kill()


class LeaderSpite(BlockSpite):

    def __init__(self, group, x, y, direction=M_STOP):
        self.group = group
        super().__init__(x, y, LEADER_BLOCK_FILE)
        s_data.s_map[x][y] = s_data.score + 1
        self.direction = direction

    def update(self):
        # 记录上一次的位置
        t_x = self.x
        t_y = self.y
        s_data.s_map[t_x][t_y] -= 1

        if self.direction == M_UP:
            if self.y - 1 < 0:
                s_data.flag = False
            else:
                self.rect.y -= BLOCK_RECT.height
                self.y -= 1
        elif self.direction == M_RIGHT:
            if self.x + 1 > MAP_X - 1:
                s_data.flag = False
            else:
                self.rect.x += BLOCK_RECT.width
                self.x += 1
        elif self.direction == M_DOWN:
            if self.y + 1 > MAP_Y - 1:
                s_data.flag = False
            else:
                self.rect.y += BLOCK_RECT.height
                self.y += 1
        elif self.direction == M_LEFT:
            if self.x - 1 < 0:
                s_data.flag = False
            else:
                self.rect.x -= BLOCK_RECT.width
                self.x -= 1
        elif self.direction == M_STOP:
            return

        # 判断是否遇到point
        if s_data.flag:
            if s_data.s_map[self.x][self.y] == -1:
                s_data.point = True
                s_data.score += 1
                s_data.s_map[t_x][t_y] += 1
                # 另取point方块

            elif s_data.s_map[self.x][self.y] > 0:
                s_data.flag = False

            # 变当前为score+1
            s_data.s_map[self.x][self.y] = s_data.score + 1
            # 在leader后增加一个方块
            if s_data.score != 0:
                self.group.add(BlockSpite(t_x, t_y))


class PointSpite(BlockSpite):

    def __init__(self):
        x, y = self.get_random()
        super().__init__(x, y, POINT_BLOCK_FILE)
        # 父类没有赋值，修改为-1和蛇的身体和其他方块区分
        s_data.s_map[x][y] = -1

    @staticmethod
    def get_random():
        x = random.randint(0, s_data.x - 1)
        y = random.randint(0, s_data.y - 1)
        while s_data.s_map[x][y] != 0:
            x = random.randint(0, s_data.x - 1)
            y = random.randint(0, s_data.y - 1)
        return x, y

    def update(self):
        if s_data.point:
            self.x, self.y = self.get_random()
            self.rect.x = self.x * BLOCK_RECT.width
            self.rect.y = self.y * BLOCK_RECT.height
            s_data.s_map[self.x][self.y] = -1
