# Breadth First Search
from maze_generator import Maze
import pygame
import time


class BFS:
    def __init__(self):
        self.parentMaze = None
        self.start = None
        self.goal = None

    def check_dead_end(self, child_cell, direction):
        if direction == 'U':  # => D
            child_cell = (child_cell[0], child_cell[1] + self.parentMaze.cell_width)
        elif direction == 'D':  # => U
            child_cell = (child_cell[0], child_cell[1] - self.parentMaze.cell_width)
        elif direction == 'L':  # => R
            child_cell = (child_cell[0] + self.parentMaze.cell_width, child_cell[1])
        elif direction == 'R':  # => L
            child_cell = (child_cell[0] - self.parentMaze.cell_width, child_cell[1])
        return child_cell

    def visited_point(self, cur_cell, child_cell, d, delay):
        if d == 'U':
            self.parentMaze.head_cell(child_cell)
            time.sleep(delay)
            
            self.parentMaze.push_up(cur_cell)
        elif d == 'D':
            self.parentMaze.head_cell(child_cell)
            time.sleep(delay)
            
            self.parentMaze.push_down(cur_cell)
        elif d == 'L':
            self.parentMaze.head_cell(child_cell)
            time.sleep(delay)
            
            self.parentMaze.push_left(cur_cell)
        elif d == 'R':
            self.parentMaze.head_cell(child_cell)
            time.sleep(delay)
            
            self.parentMaze.push_right(cur_cell)

    def bfs(self, parent_maze=Maze(), start=(0, 0), goal=(0, 0), delay=0.01):
        self.parentMaze = parent_maze
        self.start = start
        self.goal = goal

        frontier = [start]
        visited = [start]
        bfsPath = {}
        while len(frontier) > 0:
            cur_cell = frontier.pop(0)
            if cur_cell == self.goal:
                break
            for d in 'UDLR':
                if self.parentMaze.maze_map[cur_cell][d] == 1:
                    if d == 'U':
                        child_cell = (cur_cell[0], cur_cell[1] - self.parentMaze.cell_width)
                        self.parentMaze.head_cell(child_cell)
                        time.sleep(delay)
                        self.parentMaze.push_up(cur_cell)
                    elif d == 'D':
                        child_cell = (cur_cell[0], cur_cell[1] + self.parentMaze.cell_width)
                        self.parentMaze.head_cell(child_cell)
                        time.sleep(delay)
                        self.parentMaze.push_down(cur_cell)
                    elif d == 'L':
                        child_cell = (cur_cell[0] - self.parentMaze.cell_width, cur_cell[1])
                        self.parentMaze.head_cell(child_cell)
                        time.sleep(delay)
                        self.parentMaze.push_left(cur_cell)
                    elif d == 'R':
                        child_cell = (cur_cell[0] + self.parentMaze.cell_width, cur_cell[1])
                        self.parentMaze.head_cell(child_cell)
                        time.sleep(delay)
                        self.parentMaze.push_right(cur_cell)

                    if child_cell in visited:
                        continue
                    frontier.append(child_cell)
                    visited.append(child_cell)
                    bfsPath[child_cell] = cur_cell

        fwdPath = {}
        cell = self.goal
        while cell != start:
            fwdPath[bfsPath[cell]] = cell
            cell = bfsPath[cell]
        return fwdPath


if __name__ == '__main__':
    m = Maze((0, 0), 10, 10, 20)
    m.create_maze()

    mouse = BFS()
    path = mouse.bfs(parent_maze=m, start=m.start, goal=m.end, delay=0.1)
    m.show_path_coordinates(path, m.start, m.end, delay=0.05)

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
