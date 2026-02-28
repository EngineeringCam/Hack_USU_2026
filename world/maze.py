import pygame

WALL = 1
FLOOR = 0
GOAL = 2

class Maze:
    def __init__(self, grid, tile_size):
        self.grid = grid
        self.tile_size = tile_size

        self.rows = len(grid)
        self.cols = len(grid[0])

        self.width = self.cols * tile_size
        self.height = self.rows * tile_size

        # Create a surface the size of the maze
        self.surface = pygame.Surface((self.width, self.height))

        # Optional: color lookup dictionary
        self.tile_colors = {
            WALL: (0, 0, 255),
            FLOOR: (30, 30, 30),
            GOAL: (0, 200, 0)
        }

        # Pre-render the maze once
        self._build_surface()

    # maze.py (add inside class Maze)

    def is_wall_at_pixel(self, x, y):
        """
        Return True if the pixel at (x, y) is a wall or outside the map.
        x,y may be floats.
        """
        # convert pixel position to tile indices
        col = int(x) // self.tile_size
        row = int(y) // self.tile_size

        # outside map -> treat as wall
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return True

        return self.grid[row][col] == WALL

    def _build_surface(self):
        """Draw all tiles onto the internal surface once."""
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.grid[row][col]
                color = self.tile_colors.get(tile, (255, 0, 255))  # fallback color

                x = col * self.tile_size
                y = row * self.tile_size

                pygame.draw.rect(
                    self.surface,
                    color,
                    (x, y, self.tile_size, self.tile_size)
                )

    def is_clear_straight_path(self, x1, y1, x2, y2):
        """
        Returns True if a straight horizontal or vertical line
        between the two pixel positions contains no walls.
        """
        col1 = int(x1) // self.tile_size
        row1 = int(y1) // self.tile_size
        col2 = int(x2) // self.tile_size
        row2 = int(y2) // self.tile_size
    
        # Must be purely horizontal OR vertical
        if row1 == row2:
            # horizontal
            start = min(col1, col2)
            end = max(col1, col2)
            for c in range(start, end + 1):
                if self.grid[row1][c] == 1:
                    return False
            return True
    
        elif col1 == col2:
            # vertical
            start = min(row1, row2)
            end = max(row1, row2)
            for r in range(start, end + 1):
                if self.grid[r][col1] == 1:
                    return False
            return True
    
        return False
    
    def has_line_of_sight(self, x1, y1, x2, y2, step=4):
        """
        Returns True if there is no wall between (x1,y1) and (x2,y2).
        Uses small step ray march.
        """
        dx = x2 - x1
        dy = y2 - y1
        dist = (dx**2 + dy**2) ** 0.5
    
        if dist == 0:
            return True
    
        steps = int(dist // step)
    
        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0
            px = x1 + dx * t
            py = y1 + dy * t
    
            if self.is_wall_at_pixel(px, py):
                return False
    
        return True

    def draw(self, screen):
        """Blit the pre-rendered surface to the screen."""
        screen.blit(self.surface, (0, 0))