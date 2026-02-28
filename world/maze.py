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
            WALL: (0, 0, 0),
            FLOOR: (150, 150, 150),
            GOAL: (0, 200, 0)
        }

        # Pre-render the maze once
        self._build_surface()

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

    def draw(self, screen):
        """Blit the pre-rendered surface to the screen."""
        screen.blit(self.surface, (0, 0))