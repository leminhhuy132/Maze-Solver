import pygame
import time
import random
from enum import Enum


class Color:
    WHITE = (255, 255, 255)
    GREEN = (100, 255, 0)
    BLUE = (0, 150, 255)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)


class Maze:
    '''This is the main class to create maze.'''
    def __init__(self, start=(0, 0), rows=10, cols=10, cell_width=20):
        """

        Args:
            start (tuple, optional): _description_. Defaults to (0, 0).
            rows (int, optional): number of rows in the maze. Defaults to 10.
            cols (int, optional): number of columns in the maze. Defaults to 10.
            cell_width (int, optional): width of cell in maze. Defaults to 20.
        """
        self.start = start
        self.h_maze = rows
        self.w_maze = cols
        self.maze_map = {}
        self.grid = [] # A list of all cells
        self.path = {} # Shortest path from start(bottom right) to goal(by default top left)
        self.cell_width = cell_width
        self._canvas = None
        self.end = ((self.w_maze-1)*self.cell_width + self.start[0], (self.h_maze-1)*self.cell_width + self.start[1])

        # Define Screen
        pygame.init()
        pygame.mixer.init()
        self.W_display = self.w_maze * self.cell_width + self.start[0] * 2
        self.H_display = self.h_maze * self.cell_width + self.start[1] * 2
        self.screen = pygame.display.set_mode((self.W_display, self.H_display))
        pygame.display.set_caption("Python Maze Generator")
        self.screen.fill(Color.WHITE)

    def build_grid(self):
        y = self.start[1]
        for i in range(0, self.h_maze):
            x = self.start[0]  # set x coordinate to start position
            for j in range(0, self.w_maze):
                pygame.draw.line(self.screen, Color.BLACK, [x, y], [x + self.cell_width, y])  # top of cell
                pygame.draw.line(self.screen, Color.BLACK, [x + self.cell_width, y], [x + self.cell_width, y + self.cell_width])  # right of cell
                pygame.draw.line(self.screen, Color.BLACK, [x + self.cell_width, y + self.cell_width], [x, y + self.cell_width])  # bottom of cell
                pygame.draw.line(self.screen, Color.BLACK, [x, y + self.cell_width], [x, y])  # left of cell
                self.grid.append((x, y))  # add cell to grid list
                x = x + self.cell_width  # move cell to new position
            y = y + self.cell_width  # start a new row
        pygame.display.update()

    def build_raw_grid(self):
        self.grid = []
        for i in range(self.start[1], self.w_maze*self.cell_width+self.start[1], self.cell_width):
            for j in range(self.start[0], self.h_maze*self.cell_width+self.start[0], self.cell_width):
                self.grid.append((i, j))
                self.maze_map[i, j] = {'U': 0, 'D': 0, 'L': 0, 'R': 0}

    def push_up(self, cur_cell):
        pygame.draw.rect(self.screen, Color.BLUE, (cur_cell[0] + 1, cur_cell[1] - self.cell_width + 1, self.cell_width - 1, 2 * self.cell_width - 1),
                         0)  # draw a rectangle twice the width of the cell
        pygame.display.update()  # to animate the wall being removed

    def push_down(self, cur_cell):
        pygame.draw.rect(self.screen, Color.BLUE, (cur_cell[0] + 1, cur_cell[1] + 1, self.cell_width - 1, 2 * self.cell_width - 1), 0)
        pygame.display.update()

    def push_left(self, cur_cell):
        pygame.draw.rect(self.screen, Color.BLUE, (cur_cell[0] - self.cell_width + 1, cur_cell[1] + 1, 2 * self.cell_width - 1, self.cell_width - 1), 0)
        pygame.display.update()

    def push_right(self, cur_cell):
        pygame.draw.rect(self.screen, Color.BLUE, (cur_cell[0] + 1, cur_cell[1] + 1, 2 * self.cell_width - 1, self.cell_width - 1), 0)
        pygame.display.update()

    def head_cell(self, cur_cell):
        pygame.draw.rect(self.screen, Color.GREEN, (cur_cell[0] + 1, cur_cell[1] + 1, self.cell_width - 2, self.cell_width - 2), 0)  # draw a single width cell
        pygame.display.update()

    def refill_head_cell(self, cur_cell):
        pygame.draw.rect(self.screen, Color.BLUE, (cur_cell[0] + 1, cur_cell[1] + 1, self.cell_width - 2, self.cell_width - 2), 0)  # used to re-colour the path after head_cell
        pygame.display.update()  # has visited cell

    def path_cell(self, cur_cell):
        pygame.draw.rect(self.screen, Color.GREEN, (cur_cell[0] + self.cell_width / 4, cur_cell[1] + self.cell_width / 4, self.cell_width / 2, self.cell_width / 2), 0)  # used to show the solution
        pygame.display.update()  # has visited cell

    def open_right(self, x, y):
        w_endMaze = self.W_display - self.start[0]
        self.maze_map[x, y]['R'] = 1
        if x + self.cell_width <= w_endMaze:
            self.maze_map[x + self.cell_width, y]['L'] = 1

    def open_left(self, x, y):
        self.maze_map[x, y]['L'] = 1
        if x - self.cell_width >= 0:
            self.maze_map[x - self.cell_width, y]['R'] = 1

    def open_up(self, x, y):
        self.maze_map[x, y]['U'] = 1
        if y - self.cell_width >= 0:
            self.maze_map[x, y - self.cell_width]['D'] = 1

    def open_down(self, x, y):
        h_endMaze = self.H_display - self.start[1]
        self.maze_map[x, y]['D'] = 1
        if y + self.cell_width <= h_endMaze:
            self.maze_map[x, y + self.cell_width]['U'] = 1

    def visualize_create_maze(self, delay=0.01):
        self.build_raw_grid()
        self.show_maze_map() # draw grid

        visited = []
        stack = []
        x = self.start[0]
        y = self.start[1]
        self.head_cell((x, y))  # starting positing of maze
        stack.append((x, y))  # place starting cell into stack
        visited.append((x, y))  # add starting cell to visited list
        while len(stack) > 0:  # loop until stack is empty
            time.sleep(delay)  # slow program now a bit
            cell = []  # define cell list
            if (x + self.cell_width, y) not in visited and (x + self.cell_width, y) in self.grid:  # right cell available?
                cell.append("right")  # if yes add to cell list

            if (x - self.cell_width, y) not in visited and (x - self.cell_width, y) in self.grid:  # left cell available?
                cell.append("left")

            if (x, y + self.cell_width) not in visited and (x, y + self.cell_width) in self.grid:  # down cell available?
                cell.append("down")

            if (x, y - self.cell_width) not in visited and (x, y - self.cell_width) in self.grid:  # up cell available?
                cell.append("up")

            if len(cell) > 0:  # check to see if cell list is empty
                cell_chosen = (random.choice(cell))  # select one of the cell randomly

                if cell_chosen == "right":  # if this cell has been chosen
                    self.push_right((x, y))  # call push_right function
                    self.path[(x + self.cell_width, y)] = x, y  # maze_map = dictionary key = new cell, other = current cell
                    x = x + self.cell_width  # make this cell the current cell
                    visited.append((x, y))  # add to visited list
                    stack.append((x, y))  # place current cell on to stack

                elif cell_chosen == "left":
                    self.push_left((x, y))
                    self.path[(x - self.cell_width, y)] = x, y
                    x = x - self.cell_width
                    visited.append((x, y))
                    stack.append((x, y))

                elif cell_chosen == "down":
                    self.push_down((x, y))
                    self.path[(x, y + self.cell_width)] = x, y
                    y = y + self.cell_width
                    visited.append((x, y))
                    stack.append((x, y))

                elif cell_chosen == "up":
                    self.push_up((x, y))
                    self.path[(x, y - self.cell_width)] = x, y
                    y = y - self.cell_width
                    visited.append((x, y))
                    stack.append((x, y))
            else:
                x, y = stack.pop()  # if no cells are available pop one from the stack

    def create_maze(self):
        self.build_raw_grid()

        visited = []
        stack = []
        x = self.start[0]
        y = self.start[1]

        stack.append((x, y))  # place starting cell into stack
        visited.append((x, y))  # add starting cell to visited list
        while len(stack) > 0:  # loop until stack is empty
            cell = []  # define cell list
            if (x + self.cell_width, y) not in visited and (x + self.cell_width, y) in self.grid:
                cell.append("R")
            if (x - self.cell_width, y) not in visited and (x - self.cell_width, y) in self.grid:
                cell.append("L")
            if (x, y + self.cell_width) not in visited and (x, y + self.cell_width) in self.grid:
                cell.append("D")
            if (x, y - self.cell_width) not in visited and (x, y - self.cell_width) in self.grid:
                cell.append("U")

            if len(cell) > 0:  # check to see if cell list is empty
                cell_chosen = (random.choice(cell))  # select one of the cell randomly

                if cell_chosen == "R":  # if this cell has been chosen
                    self.open_right(x, y)
                    self.path[(x + self.cell_width, y)] = x, y
                    x = x + self.cell_width
                    visited.append((x, y))
                    stack.append((x, y))

                elif cell_chosen == "L":
                    self.open_left(x, y)
                    self.path[(x - self.cell_width, y)] = x, y
                    x = x - self.cell_width
                    visited.append((x, y))
                    stack.append((x, y))

                elif cell_chosen == "D":
                    self.open_down(x, y)
                    self.path[(x, y + self.cell_width)] = x, y
                    y = y + self.cell_width
                    visited.append((x, y))
                    stack.append((x, y))

                elif cell_chosen == "U":
                    self.open_up(x, y)
                    self.path[(x, y - self.cell_width)] = x, y
                    y = y - self.cell_width
                    visited.append((x, y))
                    stack.append((x, y))
            else:
                x, y = stack.pop()  # if no cells are available pop one from the stack
        self.show_maze_map()

    def show_maze_map(self):
        if self.grid is not None:
            for cell in self.grid:
                x, y = cell
                w = self.cell_width

                if self.maze_map[cell]['U'] == 0:
                    pygame.draw.line(self.screen, Color.BLACK, [x, y], [x+w, y])
                if self.maze_map[cell]['D'] == 0:
                    pygame.draw.line(self.screen, Color.BLACK, [x, y+w], [x+w, y+w])
                if self.maze_map[cell]['L'] == 0:
                    pygame.draw.line(self.screen, Color.BLACK, [x, y], [x, y+w])
                if self.maze_map[cell]['R'] == 0:
                    pygame.draw.line(self.screen, Color.BLACK, [x+w, y], [x+w, y+w])
        pygame.display.update()

    def plot_route_back(self, end, delay=0.01):
        x = end[0]
        y = end[1]
        self.path_cell(end) 
        while (x, y) != self.start:
            x, y = self.path[x, y] 
            self.path_cell((x, y))
            time.sleep(delay)

    def show_path_directions(self, path, start, delay=0.01):
        """Shows the path found in maze
        path = [step_1_direction, step_2_direction]
        """
        x = start[0]
        y = start[1]
        self.path_cell(start)
        for d in path:
            if d == 'U':
                y = y - self.cell_width
                self.path_cell((x, y))
            if d == 'D':
                y = y + self.cell_width
                self.path_cell((x, y))
            if d == 'L':
                x = x - self.cell_width
                self.path_cell((x, y))
            if d == 'R':
                x = x + self.cell_width
                self.path_cell((x, y))
            time.sleep(delay)

    def show_path_coordinates(self, path, start, end, delay=0.01):
        """Shows the path found in maze
        path = {cur_coordinate:next_coordinate}
        """
        x = start[0]
        y = start[1]
        self.path_cell(start)  # solution list contains all the coordinates to route back to start
        while (x, y) != end:  # loop until cell position == start position4
            x, y = path[x, y]  # "key value" now becomes the new key
            self.path_cell((x, y))  # animate route back
            time.sleep(0.1)


if __name__ == "__main__":
    m = Maze(start=(10, 10), rows=25, cols=25, cell_width=20)
    # m.create_maze()
    m.visualize_create_maze(delay=0.5)
    m.plot_route_back(m.end)

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
