"""Shared configuration and UI asset helpers.

The settings object stores display dimensions, sprite dimensions, timing values,
team spawn positions, tile dimensions, and the project root path used to load
assets. It is implemented as a singleton so that the same runtime configuration
is reused consistently across controllers, models, and views.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
from pathlib import Path
import pygame

class SingletonMeta(type):
    """Metaclass that provides one shared instance per class.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Return the singleton instance for the requested class.
        
        Returns:
            object: Shared singleton instance for the requested class."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Settings(metaclass=SingletonMeta):
    """Singleton configuration object shared across the project.
    
    Attributes:
        width (int): Display width in pixels.
        height (int): Display height in pixels.
        path (str): Project root path used to load assets.
        zoom (float): Global scale factor for sprites and tiles.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self):
        """Initialize display, timing, sprite, tile, team, and path configuration.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.screen_width = 800
        self.screen_height = 600
        self.fps = 30
        self.sprite_width = 120
        self.sprite_height = 120
        self.animation_speed = 120
        self.effect_speed = 80
        self.tile_width = 16
        self.tile_height = 16
        self.nb_tiles_width = 50
        self.nb_tiles_height = 20
        self.tiles = {'movement_range': [], 'effect_zone': [], 'effect_range': []}
        self.nb_units_per_player = 3
        self.team_indexes = {0: [(50, 50), (150, 50), (250, 50)], 1: [(10, 500), (50, 500), (100, 500)]}
        self.zoom = 2
        self.path = Path(__file__).resolve().parents[1]

    def update_resolution(self, width, height):
        """Update the stored display resolution.
        
        Args:
            width: New display width in pixels.
            height: New display height in pixels.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Updates stored display dimensions."""
        self.screen_width = width
        self.screen_height = height

    def create_ui_element(self, name, size, x, y):
        """Load, scale, and position a UI asset.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
            size: Target size used when scaling the UI element.
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
        
        Returns:
            tuple[pygame.Surface, pygame.Rect]: Loaded image and positioned rectangle.
        
        Side Effects:
            Loads an image from disk and scales it for UI rendering."""
        ui_element = pygame.image.load(f'{self.path}/assets/ui/{name}.png')
        ui_element = pygame.transform.scale(ui_element, size)
        ui_element_rect = ui_element.get_rect()
        ui_element_rect.x, ui_element_rect.y = (x, y)
        return (ui_element, ui_element_rect)
