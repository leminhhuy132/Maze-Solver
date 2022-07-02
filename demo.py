from maze_generator import *


if __name__ == "__main__":
    m = Maze(xstart=10, ystart=10, rows=25, cols=25, cell_width=20)
    m.build_raw_grid()
    m.CreateRawMaze()
    # print('Maze map')
    # for cell in m.maze_map.keys():
    #     print('{}:{}'.format(cell, m.maze_map[cell]))

    # print('Path')
    # for cell in m.path.keys():
    #     print('{}:{}'.format(cell, m.path[cell]))

    m.DrawMaze()
    # m.CreateMaze()
    m.plot_route_back(90, 90)


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
