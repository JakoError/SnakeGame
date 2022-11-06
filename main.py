import pygame
import snake_spites as game


class SnakeGame(object):
    """主游戏"""

    def __init__(self):
        print("loading...")

        # create screen
        self.screen = pygame.display.set_mode(game.SCREEN_RECT.size)
        # create clock
        self.clock = pygame.time.Clock()
        # create leader sprite
        self.__create_leader_sprite()
        # set timer speed
        pygame.time.set_timer(game.MOVE_EVENT, 75)

        self.start_game()

    def __create_leader_sprite(self):
        self.group = pygame.sprite.Group()
        bg = game.Background()
        self.leader = game.LeaderSpite(self.group, int(game.MAP_X/2 - 1), int(game.MAP_Y/2 - 1))
        self.point = game.PointSpite()
        self.group.add(bg, self.leader, self.point)
        self.group.update()
        self.group.draw(self.screen)

    def start_game(self):
        print("Start!!!")

        while True:
            # 设置刷新
            self.clock.tick(game.FRAME_PER_SEC)
            # 监听
            self.__event_handler()

    def __event_handler(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__exit_game()

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP]:
                self.leader.direction = game.M_UP
            elif keys_pressed[pygame.K_DOWN]:
                self.leader.direction = game.M_DOWN
            elif keys_pressed[pygame.K_RIGHT]:
                self.leader.direction = game.M_RIGHT
            elif keys_pressed[pygame.K_LEFT]:
                self.leader.direction = game.M_LEFT

            if event.type == game.MOVE_EVENT:
                self.__update_sprites()

    def __update_sprites(self):
        self.group.update()
        # 不渲染直接退出
        if not game.s_data.flag:
            self.__exit_game()

        # 取消point标注
        if game.s_data.point:
            game.s_data.point = False

        self.group.draw(self.screen)
        pygame.display.update()

    @staticmethod
    def __exit_game():
        print("game over")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = SnakeGame()
