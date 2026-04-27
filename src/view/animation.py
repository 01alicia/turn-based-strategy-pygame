"""Unit animation view model.

This module loads a unit sprite sheet, extracts animation frames, advances the
current frame according to elapsed time, and computes grid tiles reachable by the
unit for movement overlays.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
import pygame
from src.settings import Settings

class Animation:
    """Rendered animation state for a single unit.
    
    The animation object owns the loaded sprite sheet, extracted frames, current
    frame index, hit rectangles, and animation state. It advances frames based on
    elapsed time and returns completion information for non-looping actions.
    
    Attributes:
        rect (pygame.Rect): Main sprite rectangle.
        feet (pygame.Rect): Collision rectangle used for map interactions.
        frame_index (int): Current frame index inside the active sequence.
        state (str): Current animation state.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self, name, x, y, frame_width, frame_height, animation_speed, sprite_conf):
        """Load a unit sprite sheet and initialize animation state.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            frame_width: Width of one frame in the sprite sheet.
            frame_height: Height of one frame in the sprite sheet.
            animation_speed: Delay threshold used before advancing to the next frame.
            sprite_conf: SpriteConfig instance describing frame indexes and effect metadata.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.sprite_sheet = pygame.image.load(f'{Settings().path}/assets/spritesheets/{name}.png')
        self.x = x
        self.y = y
        self.frames = []
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(self.x + self.rect.width * 0.7 / 4, self.y + self.rect.height * 0.75, 0.45 * self.rect.width, 0.15 * self.rect.height)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.type = 'idle'
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.time_since_last_frame = 0
        self.frames = self.extract_frames(self.sprite_sheet, 8, 3)
        self.sprite_conf = sprite_conf
        self.state = 'idle'

    @property
    def image(self):
        """Current image associated with the object.
        
        Returns:
            pygame.Surface | None: Current image surface.
        
        Side Effects:
            Replaces the current image surface."""
        return self.__image

    @image.setter
    def image(self, image):
        """Current image associated with the object.
        
        Args:
            image: Pygame surface to store as the current image.
        
        Returns:
            pygame.Surface | None: Current image surface.
        
        Side Effects:
            Replaces the current image surface."""
        self.__image = image

    def get_image(self, x, y):
        """Extract a fixed-size frame from the sprite sheet.
        
        Args:
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        image = pygame.Surface([120, 120])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 120, 120))
        return image

    def extract_frames(self, sprite_sheet, num_cols, num_rows, start_col=0, start_row=0):
        """Extract frames from a grid-based sprite sheet.
        
        Args:
            sprite_sheet: Pygame surface containing animation frames.
            num_cols: Number of columns in the sprite-sheet grid.
            num_rows: Number of rows in the sprite-sheet grid.
            start_col: First column index to extract from the sprite sheet.
            start_row: First row index to extract from the sprite sheet.
        
        Returns:
            list[pygame.Surface]: Extracted frames in traversal order."""
        frames = []
        w, h = sprite_sheet.get_size()
        frame_width = w / num_cols
        frame_height = h / num_rows
        if frame_width > 120:
            frame_width = 120
        if frame_height > 120:
            frame_height = 120
        for j in range(start_row, num_rows):
            for i in range(start_col, num_cols):
                x = i * frame_width
                y = j * frame_height
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self, dt, orientation='right'):
        """Advance the current animation frame.
        
        Args:
            dt: Elapsed time since the previous frame, used to advance animations.
            orientation: Rendering orientation, typically right or left for mirrored sprites.
        
        Returns:
            bool | None: For animations and effects, indicates completion or active playback; for rendering/update controllers, no explicit value is returned.
        
        Side Effects:
            Mutates animation, effect, terrain, and rendering state depending on the object.
        
        Notes:
            The method is part of the frame loop and is expected to be called repeatedly."""
        if self.state == 'dead':
            self.frame_index = 0
            self.__image = self.frames[self.sprite_conf.get_indexes('dead').get('dead')[self.frame_index]]
            if orientation == 'left':
                self.image = pygame.transform.flip(self.__image, True, False)
        else:
            self.time_since_last_frame += dt
            if self.time_since_last_frame >= self.animation_speed:
                if self.state == 'movement' or self.state == 'idle':
                    self.frame_index = (self.frame_index + 1) % len(self.sprite_conf.get_indexes(self.state).get(self.type))
                else:
                    self.frame_index = self.frame_index + 1
                    if self.frame_index >= len(self.sprite_conf.get_indexes(self.state).get(self.type)):
                        self.frame_index = 0
                        self.time_since_last_frame = 0
                        self.state = 'idle'
                        self.type = 'idle'
                        return True
                self.__image = self.frames[self.sprite_conf.get_indexes(self.state).get(self.type)[self.frame_index]]
                if orientation == 'left':
                    self.image = pygame.transform.flip(self.__image, True, False)
                self.time_since_last_frame = 0
        return False

    def get_walkable_tiles(self, movement_range):
        """Compute grid coordinates reachable from the animation rectangle.
        
        Args:
            movement_range: Movement-range tuple used to compute reachable tiles.
        
        Returns:
            list[tuple[int, int]]: Grid coordinates reachable from the current animation position."""
        settings = Settings()
        vertical, horizontal, diagonal = movement_range
        center_x = self.rect.x + self.rect.width / 2
        center_y = self.rect.y + self.rect.height / 2
        tile_x = int(center_x / (settings.tile_width * settings.zoom))
        tile_y = int(center_y / (settings.tile_width * settings.zoom))
        walkable_tiles = []
        for dy in range(-vertical, vertical + 1):
            walkable_tiles.append((tile_x, tile_y + dy))
        for dx in range(-horizontal, horizontal + 1):
            walkable_tiles.append((tile_x + dx, tile_y))
        for d in range(-diagonal, diagonal + 1):
            if d != 0:
                walkable_tiles.append((tile_x + d, tile_y + d))
                walkable_tiles.append((tile_x + d, tile_y - d))
        return walkable_tiles
