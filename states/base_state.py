# states/base_state.py

class BaseState:
    """
    Base class for all game states.
    Every state should inherit from this and override its methods.
    """

    def handle_events(self, game, event):
        """
        Handle discrete input (keyboard, mouse, etc.).
        Called once per event per frame.
        """
        pass

    def update(self, game, dt):
        """
        Update game logic.
        dt = delta time in seconds.
        Called once per frame.
        """
        pass

    def draw(self, game, screen):
        """
        Draw everything for this state.
        Called once per frame after update().
        """
        pass