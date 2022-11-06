class Data(object):
    x = 32
    y = 32

    def __init__(self):
        self.s_map = []
        self.create_map()
        self.score = 0
        self.flag = True
        self.point = False
        # self.timer = time.ctime()

    def create_map(self):
        row = []
        for i in range(Data.y):
            row.append(0)
        for i in range(Data.x):
            self.s_map.append(row.copy())
