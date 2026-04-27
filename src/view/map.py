"""Map loading and rendering utilities.

The map view loads TMX data, builds the scrolling renderer, extracts collision
and terrain rectangles, draws visible tile layers, and displays movement overlays
used by the active unit.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
import pygame
import pytmx
import pyscroll
from src.settings import Settings
from src.view.screen import Screen

class Map:
    """TMX-backed battlefield renderer and terrain data provider.
    
    Attributes:
        collisions (list[pygame.Rect]): Blocking map objects.
        ice (list[pygame.Rect]): Ice terrain rectangles.
        lava (list[pygame.Rect]): Lava terrain rectangles.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self, screen: Screen, zoom_factor=2):
        """Load the default map and prepare terrain rectangles.
        
        Args:
            screen (Screen): Pygame surface or screen wrapper used as the drawing target.
            zoom_factor: Scale factor applied to map rendering.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.__screen = screen
        self.__tmx_data = None
        self.__map_layer = None
        self.__group = None
        self.__zoom_factor = zoom_factor
        self.switch_map('map_1')
        self.__collisions = []
        self.get_collisions()
        self.ice_tiles = []
        self.lava_tiles = []
        self.get_tiles()

    @property
    def screen(self):
        """Screen wrapper used for rendering.
        
        Returns:
            Screen: Screen wrapper used for rendering."""
        return self.__screen

    @property
    def tmx_data(self):
        """Loaded TMX map data.
        
        Returns:
            pytmx.TiledMap: Loaded TMX map data."""
        return self.__tmx_data

    @property
    def map_layer(self):
        """Buffered map renderer.
        
        Returns:
            pyscroll.BufferedRenderer: Renderer used for tiled map drawing."""
        return self.__map_layer

    @property
    def group(self):
        """Pyscroll rendering group.
        
        Returns:
            pyscroll.PyscrollGroup: Rendering group combining map and sprites."""
        return self.__group

    @property
    def zoom_factor(self):
        """Map zoom factor.
        
        Returns:
            float: Current map zoom factor."""
        return self.__zoom_factor

    @property
    def collisions(self):
        """Collision rectangles extracted from map objects.
        
        Returns:
            list[pygame.Rect]: Collision rectangles extracted from the map."""
        return self.__collisions

    @property
    def width(self):
        """Renderable map width in pixels.
        
        Returns:
            int: Map width in pixels."""
        setting = Settings()
        return setting.tile_width * (setting.nb_tiles_width - 1) * self.__zoom_factor

    @property
    def height(self):
        """Renderable map height in pixels.
        
        Returns:
            int: Map height in pixels."""
        setting = Settings()
        return setting.tile_height * (setting.nb_tiles_height - 1) * self.__zoom_factor

    def switch_map(self, map: str):
        """Load a TMX map and rebuild the scroll renderer.
        
        Args:
            map (str): Map file name or path to load.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Loads a TMX map and rebuilds the scroll renderer and terrain data."""
        self.__tmx_data = pytmx.load_pygame(f'{Settings().path}/assets/map/{map}.tmx')
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.__map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = self.__zoom_factor
        self.__group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

    def update(self, animation_manager, current_unit):
        """Draw visible map layers and delegate unit rendering at the player layer.
        
        Args:
            animation_manager: AnimationManager coordinating unit animations and effects.
            current_unit: Unit whose turn is currently active.
        
        Returns:
            bool | None: For animations and effects, indicates completion or active playback; for rendering/update controllers, no explicit value is returned.
        
        Side Effects:
            Mutates animation, effect, terrain, and rendering state depending on the object.
        
        Notes:
            The method is part of the frame loop and is expected to be called repeatedly."""
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile is not None:
                        zoomed_tile = pygame.transform.scale(tile, (int(self.tmx_data.tilewidth * self.zoom_factor), int(self.tmx_data.tileheight * self.zoom_factor)))
                        zoomed_x = x * self.tmx_data.tilewidth * self.zoom_factor
                        zoomed_y = y * self.tmx_data.tileheight * self.zoom_factor
                        self.screen.display.blit(zoomed_tile, (zoomed_x, zoomed_y))
            if layer.name == 'PlayerLayer':
                animation_manager.draw(self.screen.display)

    def get_collisions(self):
        """Extract collision rectangles from TMX objects.
        
        Returns:
            list[pygame.Rect]: Collision rectangles extracted from TMX objects."""
        for obj in self.tmx_data.objects:
            if obj.type == 'collision':
                self.collisions.append(pygame.Rect(obj.x * self.zoom_factor, obj.y * self.zoom_factor, obj.width * self.zoom_factor, obj.height * self.zoom_factor))

    def get_tiles(self):
        """Extract special terrain rectangles such as ice and lava from TMX objects.
        
        Returns:
            dict[str, list[pygame.Rect]]: Terrain rectangles grouped by terrain type."""
        for obj in self.tmx_data.objects:
            if obj.type == 'Ice':
                self.ice_tiles.append(pygame.Rect(obj.x * self.zoom_factor, obj.y * self.zoom_factor, obj.width * self.zoom_factor, obj.height * self.zoom_factor))
            elif obj.type == 'Lava':
                self.lava_tiles.append(pygame.Rect(obj.x * self.zoom_factor, obj.y * self.zoom_factor, obj.width * self.zoom_factor, obj.height * self.zoom_factor))

    def draw_walkable_overlay(self, walkable_tiles):
        """Draw translucent overlays on the tiles reachable by the active unit.
        
        Args:
            walkable_tiles: Iterable of tile coordinates to highlight.
        
        Returns:
            None: This method is executed for its side effects."""
        settings = Settings()
        for x, y in walkable_tiles:
            tile_x = x * settings.tile_width * self.zoom_factor
            tile_y = y * settings.tile_height * self.zoom_factor
            overlay_color = (0, 255, 0, 128)
            overlay_surface = pygame.Surface((int(settings.tile_width * self.zoom_factor), int(settings.tile_height * self.zoom_factor)), pygame.SRCALPHA)
            overlay_surface.fill(overlay_color)
            self.screen.display.blit(overlay_surface, (tile_x, tile_y))

    def overlay_tile(self, x, y, color):
        """Draw a translucent overlay on a single tile coordinate.
        
        Args:
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            color: Text color passed to Pygame rendering APIs.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Draws a translucent overlay on the map layer surface."""
        settings = Settings()
        overlay_surface = pygame.Surface((settings.tile_width, settings.tile_height), pygame.SRCALPHA)
        overlay_surface.fill(color)
        self.screen.display.blit(overlay_surface, (x * settings.tile_width, y * settings.tile_height))
