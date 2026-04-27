"""
Core package for the turn-based strategy game.

This package contains the main application layers used by the game:

Modules:
    settings: Global runtime configuration shared across the project.

Packages:
    controller: Input handling, menu control, and animation orchestration.
    model: Gameplay entities, players, units, abilities, and factories.
    view: Rendering components, animations, menus, sprites, and map display.

The project follows a lightweight Model-View-Controller organization:

- The model layer stores game state and gameplay rules.
- The view layer renders visual elements through Pygame.
- The controller layer coordinates user input and game-flow actions.
"""

# from .settings import Settings, SingletonMeta
#
# __all__ = [
#     "Settings",
#     "SingletonMeta",
# ]