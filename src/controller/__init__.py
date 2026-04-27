"""
Controller layer for game-flow coordination.

The controller package contains components that translate user input and
game state changes into concrete gameplay actions. Controllers are responsible
for coordinating interactions between the model layer and the view layer
without owning the core gameplay data themselves.

Modules:
    animation_manager:
        Coordinates animation execution and visual feedback during actions.

    menu_handler:
        Handles menu navigation, selection flow, and menu-related input.

    player_handler:
        Processes player input and maps it to gameplay commands.

Public Classes:
    AnimationManager:
        Manages action animations and synchronization with game state.

    MenuHandler:
        Coordinates menu interactions and user choices.

    PlayerHandler:
        Handles player-side interactions and turn-based action selection.
"""

# from .animation_manager import AnimationManager
# from .menu_handler import MenuHandler
# from .player_handler import PlayerHandler
#
# __all__ = [
#     "AnimationManager",
#     "MenuHandler",
#     "PlayerHandler",
# ]