"""
View layer for rendering and visual presentation.

The view package contains the rendering components used by the game. It
defines visual abstractions for animations, effects, maps, menus, screens,
and sprite configuration. These components are responsible for presentation
and should not own core gameplay rules.

Modules:
    animation:
        Defines frame-based animation behavior.

    animation_factory:
        Builds animation objects from sprite and configuration data.

    effect:
        Represents visual effects displayed during abilities or actions.

    map:
        Handles map rendering and tile-based display logic.

    menu:
        Provides menu rendering and visual menu state.

    screen:
        Manages the main display surface and screen-level rendering helpers.

    sprites_config:
        Stores sprite-sheet frame configuration for units and actions.

Public Classes:
    Animation:
        Represents a frame-based visual animation.

    AnimationFactory:
        Creates animations from sprite configuration data.

    Effect:
        Represents an independent visual effect.

    Map:
        Renders and manages the visual map representation.

    Menu:
        Displays interactive menu options.

    Screen:
        Wraps screen-level rendering operations.

    SpriteConfig:
        Stores frame indexes and sprite metadata.
"""

# from .animation import Animation
# from .animation_factory import AnimationFactory
# from .effect import Effect
# from .map import Map
# from .menu import Menu
# from .screen import Screen
# from .sprites_config import SpriteConfig

# __all__ = [
#     "Animation",
#     "AnimationFactory",
#     "Effect",
#     "Map",
#     "Menu",
#     "Screen",
#     "SpriteConfig",
# ]