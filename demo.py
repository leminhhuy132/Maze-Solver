import pygame

from maze_generator import Maze
from Demos.BFS.BFS import BFS
from Demos.DFS.DFS import DFS
from Demos.Wall_follower.wall_follower import WallFollower

if __name__ == "__main__":
    m = Maze(start=(10,10), rows=25, cols=25, cell_width=20)
    m.create_maze()
    # m.visualize_create_maze()
    
    # mouse = BFS()
    # path = mouse.bfs(parent_maze=m, start=m.start, goal=m.end, delay=0.1)

    # mouse = DFS()
    # path = mouse.dfs(parent_maze=m, start=m.start, goal=m.end, delay=0.1)
    # m.show_path_coordinates(path, m.start, m.end, delay=0.01)

    mouse = WallFollower()
    path = mouse.wall_follower(parent_maze=m, start=m.start, goal=m.end, delay=0.1)
    m.show_path_directions(path, m.start, delay=0.01)

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
