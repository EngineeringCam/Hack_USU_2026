class Maze:

    TILE_SIZE = 64

    PATH = 0
    WALL = 1

    ROWS = len(maze)
    COLUMNS = len(maze[0])

    MAP_HEIGHT = TILE_SIZE * ROWS
    MAP_WIDTH = TILE_SIZE * COLUMNS

    for row in range(ROWS):
        for column in range(COLUMNS):
            if maze[row][column] == 1:
                pygame.draw.rect(
                    screen,
                    (0, 0, 0)
                    (column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )
    
    player_x = TILE_SIZE / 2
    player_y = TILE_SIZE / 2
    player_speed = 5

    grid_x = player_x // TILE_SIZE
    grid_y = player_y // TILE_SIZE