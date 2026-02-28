import pygame

class Player:
    def __init__(self, x, y, size=28, speed=180):
        # Position stored as floats for smooth movement
        self.x = float(x)
        self.y = float(y)

        self.size = size
        self.speed = speed  # pixels per second

        self.color = (255, 50, 50)

    def get_rect(self):
        """Return a pygame.Rect representing the player's hitbox."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, dt, maze, dx, dy):
        """
        dt   = delta time (seconds)
        maze = Maze object (for collision)
        dx/dy = direction input (-1, 0, or 1)
        """

        # Normalize diagonal movement (prevents faster diagonal speed)
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        # Calculate movement amount
        move_x = dx * self.speed * dt
        move_y = dy * self.speed * dt

        # --- Move in X direction first ---
        self.x += move_x
        if self._collides_with_wall(maze):
            # Undo movement if collision
            self.x -= move_x

        # --- Then move in Y direction ---
        self.y += move_y
        if self._collides_with_wall(maze):
            self.y -= move_y

    def _collides_with_wall(self, maze):
        """Check collision against maze walls using tile lookup."""
        rect = self.get_rect()

        # Determine which tiles the player overlaps
        left_tile = rect.left // maze.tile_size
        right_tile = rect.right // maze.tile_size
        top_tile = rect.top // maze.tile_size
        bottom_tile = rect.bottom // maze.tile_size

        for row in range(int(top_tile), int(bottom_tile) + 1):
            for col in range(int(left_tile), int(right_tile) + 1):

                # Bounds check
                if row < 0 or row >= maze.rows or col < 0 or col >= maze.cols:
                    return True  # treat outside map as wall

                # Check tile type, if 1, it's a wall
                if maze.grid[row][col] == 1:
                    return True

        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())