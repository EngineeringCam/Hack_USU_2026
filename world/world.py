import pygame

from states.playing_state import PlayingState


class Game:
    """
    Owns the pygame window + clock and delegates behavior to the active State.
    """

    def __init__(self, width: int, height: int, caption: str = "Maze Game", fps: int = 60):
        # Window / timing
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

        # FSM: start in Playing for now
        self.current_state = PlayingState()

    def change_state(self, new_state) -> None:
        """Switch to a new state object (e.g., MenuState(), PauseState())."""
        self.current_state = new_state

    def handle_events(self) -> None:
        """Collect pygame events and forward them to the current state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Let the active state respond to events (keys, mouse, etc.)
            if self.current_state is not None:
                self.current_state.handle_events(self, event)

    def update(self) -> float:
        """
        Tick the clock and update the current state.
        Returns dt in seconds.
        """
        dt_seconds = self.clock.tick(self.fps) / 1000.0

        if self.current_state is not None:
            self.current_state.update(self, dt_seconds)

        return dt_seconds

    def draw(self) -> None:
        """Clear the screen, ask the state to draw, then present the frame."""
        self.screen.fill((0, 0, 0))

        if self.current_state is not None:
            self.current_state.draw(self, self.screen)

        pygame.display.flip()