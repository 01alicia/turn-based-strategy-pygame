"""Visual effect view model.

Effects are loaded from external sprite sheets when configured for a competence.
The class extracts frames, advances effect playback, optionally interpolates
projectile movement toward a target, and draws the active effect on the screen.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
import numpy as np
import pygame
from src.settings import Settings

class Effect:
    """Runtime state for a visual competence effect.
    
    An effect can be attached to an attack or defense. It stores the selected frame
    sequence, playback position, screen coordinates, and optional interpolation path
    for moving effects.
    
    Attributes:
        current_effect (tuple | None): Metadata of the active effect.
        effect_frames (list[pygame.Surface]): Frames of the active effect.
        effect_x (list | numpy.ndarray | None): Horizontal playback positions.
        effect_y (list | numpy.ndarray | None): Vertical playback positions.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self, sprite_conf, animation_speed):
        """Initialize effect playback state and load configured effect sprite sheets.
        
        Args:
            sprite_conf: SpriteConfig instance describing frame indexes and effect metadata.
            animation_speed: Delay threshold used before advancing to the next frame.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.sprite_conf = sprite_conf
        self.effects = {}
        self.set_effects()
        self.current_effect = None
        self.effect_frames = []
        self.effect_x = None
        self.effect_y = None
        self.effect_image = None
        self.__effect_index = 0
        self.type = None
        self.time_since_last_effect = 0
        self.animation_speed = animation_speed

    def set_effects(self):
        """Load external effect sprite sheets declared by the sprite configuration.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Loads configured effect sprite sheets from disk."""
        for effect_name in self.sprite_conf.effects.keys():
            self.effects[effect_name] = pygame.image.load(f'{Settings().path}/assets/spritesheets/{effect_name}.png')

    def reset_effect(self):
        """Clear the active effect and reset playback indexes.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Clears active effect state and resets playback counters."""
        self.current_effect = None
        self.effect_frames = []
        self.effect_x = None
        self.effect_y = None
        self.effect_image = None
        self.__effect_index = 0
        self.time_since_last_effect = 0

    def apply_effect(self, dt, orientation='right'):
        """Advance the active effect playback.
        
        Args:
            dt: Elapsed time since the previous frame, used to advance animations.
            orientation: Rendering orientation, typically right or left for mirrored sprites.
        
        Returns:
            bool: ``True`` while the effect is still active; ``False`` when it has ended or is inactive.
        
        Side Effects:
            Advances effect frame counters and may clear the active effect."""
        if self.current_effect is not None and self.effect_x is not None and (self.effect_y is not None):
            self.time_since_last_effect += dt
            if self.time_since_last_effect >= self.animation_speed:
                self.time_since_last_effect = 0
                self.__effect_index += 1
                if self.__effect_index >= len(self.effect_frames):
                    self.reset_effect()
                    return False
            self.effect_image = self.effect_frames[self.__effect_index]
            if orientation == 'left':
                self.effect_image = pygame.transform.flip(self.effect_image, True, False)
            return True
        return False

    def update(self, x, y, state, type, target_pos=None):
        """Select and position the effect matching a competence activation.
        
        Args:
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            state: Gameplay or animation state to apply.
            type: Action subtype, competence name, or category key used by the caller.
            target_pos: Optional target position used to place or interpolate a visual effect.
        
        Returns:
            bool | None: For animations and effects, indicates completion or active playback; for rendering/update controllers, no explicit value is returned.
        
        Side Effects:
            Mutates animation, effect, terrain, and rendering state depending on the object.
        
        Notes:
            The method is part of the frame loop and is expected to be called repeatedly."""
        if self.current_effect is None and type in self.sprite_conf.effects:
            self.type = type
            self.current_effect = self.sprite_conf.effects[type]
            self.effect_frames = self.extract_frames(self.effects[type], self.current_effect[3], self.current_effect[3], self.current_effect[0], self.current_effect[1])
            if state == 'attacks':
                if target_pos is not None:
                    if self.current_effect[2]:
                        self.effect_x = np.linspace(x, target_pos[0], len(self.effect_frames))
                        self.effect_y = np.linspace(y, target_pos[1], len(self.effect_frames))
                    else:
                        self.effect_x = [target_pos[0]]
                        self.effect_y = [target_pos[1]]
                else:
                    self.current_effect = None
            elif state == 'defenses':
                if self.current_effect[2]:
                    if target_pos is not None:
                        self.effect_x = [target_pos[0]]
                        self.effect_y = [target_pos[1]]
                    else:
                        self.current_effect = None
                else:
                    self.effect_x = [x]
                    self.effect_y = [y]
            else:
                self.current_effect = None
            print(f'Interpolation X: {self.effect_x}, Y: {self.effect_y}')
            self.__effect_index = 0
            self.time_since_last_effect = 0
            self.effect_image = self.effect_frames[self.__effect_index]

    def draw(self, screen):
        """Draw the current effect frame on the provided surface.
        
        Args:
            screen: Pygame surface or screen wrapper used as the drawing target.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Blits animation and effect frames to the target surface."""
        if self.effect_image is None or self.effect_x is None or self.effect_y is None:
            return
        if len(self.effect_x) == 0 or len(self.effect_y) == 0:
            return
        x = self.effect_x[self.__effect_index % len(self.effect_x)]
        y = self.effect_y[self.__effect_index % len(self.effect_y)]
        screen.blit(self.effect_image, (x, y))

    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_cols, num_rows, start_col=0, start_row=0):
        """Extract and scale effect frames from a sprite sheet.
        
        Args:
            sprite_sheet: Pygame surface containing animation frames.
            frame_width: Width of one frame in the sprite sheet.
            frame_height: Height of one frame in the sprite sheet.
            num_cols: Number of columns in the sprite-sheet grid.
            num_rows: Number of rows in the sprite-sheet grid.
            start_col: First column index to extract from the sprite sheet.
            start_row: First row index to extract from the sprite sheet.
        
        Returns:
            list[pygame.Surface]: Extracted frames in traversal order."""
        frames = []
        scale = 0.7
        for j in range(start_row, num_rows):
            for i in range(start_col, num_cols):
                x = i * frame_width
                y = j * frame_height
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                if frame_width > 150:
                    scale = 0.6
                frame = pygame.transform.scale(frame, (int(frame.get_width() * scale), int(frame.get_height() * scale)))
                frames.append(frame)
        return frames
