import matplotlib.pyplot as plt
import copy
import matplotlib.style as mplstyle

mplstyle.use('fast')


class Cord:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Cord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        return Cord(self.x * other, self.y * other, self.z * other)


class Node:
    def __init__(self, x, y, z):
        self.coord = Cord(x, y, z)

    G = 0
    H = 0
    collision = False
    parent = None


def find_on_list(data, val):
    return val if val in data else None


def heuristic(start, end):
    return (abs(start.coord.x - end.coord.x) + abs(start.coord.y - end.coord.y) + abs(
        start.coord.z - end.coord.z)) * 10


class A_STAR:
    def __init__(self, length=10, width=10, height=10):
        self.length = length
        self.width = width
        self.height = height
        row = []
        for i in range(length):
            row.append(Node(0, 0, 0))
        col = []
        for i in range(width):
            col.append(copy.deepcopy(row))
        self.world = []
        for i in range(height):
            self.world.append(copy.deepcopy(col))

        for z, i in enumerate(self.world):
            for y, j in enumerate(i):
                for x, k in enumerate(j):
                    k.coord.x = x
                    k.coord.y = y
                    k.coord.z = z
        self.directions = 26
        self.direction = [
            Cord(1, 0, 0), Cord(-1, 0, 0),  # 1
            Cord(0, 1, 0), Cord(0, -1, 0),
            Cord(0, 0, 1), Cord(0, 0, -1),

            Cord(1, 1, 0), Cord(-1, 1, 0),  # 2
            Cord(1, -1, 0), Cord(-1, -1, 0),

            Cord(1, 0, 1), Cord(-1, 0, 1),
            Cord(0, 1, 1), Cord(0, -1, 1),
            Cord(1, 0, -1), Cord(-1, 0, -1),
            Cord(0, 1, -1), Cord(0, -1, -1),

            Cord(1, 1, 1), Cord(-1, 1, 1),  # 3
            Cord(1, -1, 1), Cord(-1, -1, 1),
            Cord(1, 1, -1), Cord(-1, 1, -1),
            Cord(1, -1, -1), Cord(-1, -1, -1),
        ]
        self.path = []
        self.block = []
        self.path_count = 0

    def add_coli(self, x, y, z):
        if x > self.length or y > self.width or z > self.height \
                or x < 0 or y < 0 or z < 0:
            return False
        else:
            self.world[z][y][x].collision = True
            self.block.append((x, y, z))
            return True

    def add_ball_block(self, x, y, z, r):
        for i in range(self.height):
            for j in range(self.width):
                for k in range(self.length):
                    if pow(k - x, 2) + pow(j - y, 2) + pow(i - z, 2) <= pow(r, 2):
                        self.add_coli(k, j, i)

    def find_path(self, start, end):
        print('Start Point:', start.coord.x, start.coord.y, start.coord.z)
        print(' End  Point:', end.coord.x, end.coord.y, end.coord.z)
        open_set = []
        close_set = []
        open_set.append(start)
        if end.collision is True and start.collision is True:
            if end.collision is True:
                print('终止点被挡住了')
            if start.collision is True:
                print('起始点被挡住了')
            return
        while len(open_set) != 0:
            open_set.sort(key=lambda x: x.G + x.H)
            current = open_set[0]
            if current.coord.x == end.coord.x and current.coord.y == end.coord.y and current.coord.z == end.coord.z:
                break
            close_set.append(current)
            open_set.remove(current)
            for i in range(self.directions):
                new_node = self.get_node(current, self.direction[i])
                if new_node is None:
                    continue
                if find_on_list(close_set, new_node) is not None or self.detect_collision(new_node):
                    continue
                g_cost = current.G + 1
                if i < 6:
                    g_cost = current.G + 1
                elif i < 18:
                    g_cost = current.G + 2
                elif i < 26:
                    g_cost = current.G + 3
                successor = find_on_list(open_set, new_node)
                if successor is None:
                    new_node.G = g_cost
                    new_node.H = heuristic(new_node, end)
                    new_node.parent = current
                    open_set.append(new_node)
                elif successor.G > g_cost:
                    successor.G = g_cost
                    successor.parent = current

        local_path = []
        back = end
        while back != start:
            local_path.append(back.coord)
            back = back.parent
        local_path.append(start.coord)
        local_path.reverse()
        self.path.append(local_path)
        self.path_count += 1
        print('Path Plan Finished')

    def detect_collision(self, val):
        for i in range(26):
            new_node = self.get_node(val, self.direction[i])
            if new_node is None:
                continue
            if new_node.collision is True:
                return True
        return val.collision

    def get_node(self, val, move):
        new_coord = val.coord + move
        if new_coord.x >= self.length or new_coord.y >= self.width or new_coord.z >= self.height \
                or new_coord.x < 0 or new_coord.y < 0 or new_coord.z < 0:
            return None
        new_node = self.world[new_coord.z][new_coord.y][new_coord.x]
        return new_node

    def visual_map(self, route):
        fig = plt.figure(figsize=(200, 200))
        ax = fig.add_subplot(1, 1, 1, projection="3d")
        data_x = [i[0] for i in self.block]
        data_y = [i[1] for i in self.block]
        data_z = [i[2] for i in self.block]
        ax.scatter(data_x, data_y, data_z, color='#282c3410')
        data_x = [i[0] for i in route]
        data_y = [i[1] for i in route]
        data_z = [i[2] for i in route]
        ax.scatter(data_x, data_y, data_z, color='r', marker='o')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.axis('equal')
        ax.grid(False)
        ax.set_title("3D UAV")
        plt.show()

    def visual_path(self):
        fig = plt.figure(figsize=(200, 200))
        ax = fig.add_subplot(1, 1, 1, projection="3d")
        for i in range(self.path_count):
            data_x = [i.x for i in self.path[i]]
            data_y = [i.y for i in self.path[i]]
            data_z = [i.z for i in self.path[i]]
            ax.scatter(data_x, data_y, data_z, marker='1', color='#e8423e')
            ax.plot(data_x[0], data_y[0], data_z[0], color='#27b1bc', marker='o')
            ax.plot(data_x[-1], data_y[-1], data_z[-1], color='#27b1bc', marker='o')
        data_x = [i[0] for i in self.block]
        data_y = [i[1] for i in self.block]
        data_z = [i[2] for i in self.block]
        ax.scatter(data_x, data_y, data_z, color='#282c3410')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.axis('equal')
        ax.grid(False)
        ax.set_title("3D A-Star UAV Navigation")
        plt.show()


example = A_STAR(100, 100, 100)
# example.add_ball_block(5, 5, 5, 5)
# example.add_ball_block(50, 50, 5, 10)
# example.add_ball_block(40, 0, 2, 10)
# example.add_ball_block(50, 50, 50, 20)
# example.add_ball_block(50, 0, 32, 15)
example.add_ball_block(10, 0, 10, 6)
example.add_ball_block(15, 0, 15, 6)
example.add_ball_block(25, 10, 25, 10)
example.add_ball_block(20, 37, 60, 20)
example.add_ball_block(10, 20, 15, 6)
example.add_ball_block(10, 30, 20, 6)
example.add_ball_block(25, 25, 25, 20)
example.add_ball_block(75, 75, 75, 20)
route = [(0, 0, 0), (45, 10, 12), (0, 20, 23), (45, 30, 45), (0, 35, 45), (89, 90, 90)]
example.visual_map(route)
for i in range(len(route) - 1):
    example.find_path(example.world[route[i][2]][route[i][1]][route[i][0]],
                      example.world[route[i + 1][2]][route[i + 1][1]][route[i + 1][0]])
example.visual_path()

#
# example = A_STAR(10, 10, 10)
# # example.add_ball_block(5, 5, 5, 5)
# # example.add_ball_block(50, 50, 5, 10)
# # example.add_ball_block(40, 0, 2, 10)
# # example.add_ball_block(50, 50, 50, 20)
# # example.add_ball_block(50, 0, 32, 15)
# example.add_ball_block(3, 3, 3, 1)
# example.add_ball_block(5, 5, 5, 6)
# example.add_ball_block(5, 10, 25, 10)
# example.add_ball_block(10, 20, 15, 6)
# example.add_ball_block(10, 30, 20, 6)
# example.add_ball_block(25, 25, 25, 20)
# example.add_ball_block(75, 75, 75, 20)
# route = [(0, 0, 0), (3, 4, 5), (0, 20, 23), (45, 30, 45), (0, 35, 45), (89, 90, 90)]
# example.visual_map(route)
# for i in range(len(route) - 1):
#     example.find_path(example.world[route[i][2]][route[i][1]][route[i][0]],
#                       example.world[route[i + 1][2]][route[i + 1][1]][route[i + 1][0]])
# example.visual_path()


# while True:
#     print('请输入选项：')
#     print('1.添加圆形障碍物')
#     print('2.添加设置路径点')
#     a = int(input())
#     print(a)
# a = Node(x=5, y=5, z=5)
# b = Node(x=6, y=5, z=5)
# c = Node(x=7, y=5, z=5)
# a.G=99
# a.H=1
# b.G=10
# b.H=2
# c.G=3
# c.H=322
#
# aaa = []
# aaa.append(c)
# aaa.append(b)
# aaa.append(a)
#
# aaa.sort(key=lambda x: x.G+x.H)
# print(aaa[0].coord.x, aaa[0].coord.y, aaa[0].coord.z)
