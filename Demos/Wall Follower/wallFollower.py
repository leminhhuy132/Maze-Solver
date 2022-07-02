from maze_generator import Maze
import pygame
import time


class WallFollower:
    def __init__(self):
        '''
        Right
        :param parent_maze: Maze
        :param start: start point
        :param goal: end point
        :return:
        '''
        self.parentMaze = None
        self.start = None
        self.goal = None
        self.direction = {'forward': 'U', 'left': 'L', 'back': 'D', 'right': 'R'}

    def RCW(self):
        k = list(self.direction.keys())
        v = list(self.direction.values())
        v_rotated = [v[-1]] + v[:-1]
        self.direction = dict(zip(k, v_rotated))

    def RCCW(self):
        k = list(self.direction.keys())
        v = list(self.direction.values())
        v_rotated = v[1:] + [v[0]]
        self.direction = dict(zip(k, v_rotated))

    def moveForward(self, cur_cell):
        w = self.parentMaze.cell_width
        if self.direction['forward'] == 'R':
            self.parentMaze.push_right(cur_cell)
            return (cur_cell[0]+w, cur_cell[1]), 'R'
        if self.direction['forward'] == 'L':
            self.parentMaze.push_left(cur_cell)
            return (cur_cell[0]-w, cur_cell[1]), 'L'
        if self.direction['forward'] == 'U':
            self.parentMaze.push_up(cur_cell)
            return (cur_cell[0], cur_cell[1]-w), 'U'
        if self.direction['forward'] == 'D':
            self.parentMaze.push_down(cur_cell)
            return (cur_cell[0], cur_cell[1]+w), 'D'

    def wall_follower(self, parent_maze=Maze(), start=(0, 0), goal=(0, 0), delay=0.01):
        self.parentMaze = parent_maze
        self.start = start
        self.goal = goal

        cur_cell = self.start
        path = ''
        while True:
            if cur_cell == self.goal:
                break
            if m.maze_map[cur_cell][self.direction['left']] == 0:
                if m.maze_map[cur_cell][self.direction['forward']] == 0:
                    self.RCW()
                else:
                    self.parentMaze.single_cell(cur_cell)
                    time.sleep(delay)
                    cur_cell, d = self.moveForward(cur_cell)
                    path += d
            else:
                self.RCCW()
                self.parentMaze.single_cell(cur_cell)
                time.sleep(delay)
                cur_cell, d = self.moveForward(cur_cell)
                path += d

        path2 = path
        while 'UD' in path2 or 'DU' in path2 or 'RL' in path2 or 'LR' in path2:
            path2 = path2.replace('DU', '')
            path2 = path2.replace('UD', '')
            path2 = path2.replace('RL', '')
            path2 = path2.replace('LR', '')
        return path, path2


if __name__ == '__main__':
    m = Maze((10, 10), 50, 50, 20)
    m.CreateRawMaze()
    m.DrawMaze()

    mouse = WallFollower()
    path, path2 = mouse.wall_follower(parent_maze=m, start=m.start, goal=m.end, delay=0)
    # print(path2)
    m.trade_path_direction(path2, m.start, delay=0)

    # ##### pygame loop #######
    clock = pygame.time.Clock()
    FPS = 30
    running = True
    while running:
        # keep running at the at the right speed
        clock.tick(FPS)
        # process input (events)
        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                running = False

