"""Pygame screen wrapper.

The screen view owns the display surface and exposes small helpers for updating
and querying the active resolution.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
import pygame

class Screen:
    """Wrapper around the active Pygame display surface.
    
    Attributes:
        screen (pygame.Surface): Active display surface.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self):
        """Create the Pygame display surface from shared settings.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.__display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Strategy Game')
        self.__clock = pygame.time.Clock()
        self.__framerate = 60

    def update(self):
        """Refresh the display surface from the current settings resolution.
        
        Returns:
            bool | None: For animations and effects, indicates completion or active playback; for rendering/update controllers, no explicit value is returned.
        
        Side Effects:
            Mutates animation, effect, terrain, and rendering state depending on the object.
        
        Notes:
            The method is part of the frame loop and is expected to be called repeatedly."""
        pygame.display.flip()
        pygame.display.update()
        self.__clock.tick(self.__framerate)
        self.__display.fill((0, 0, 0))

    def get_size(self):
        """Return the current configured display size.
        
        Returns:
            tuple[int, int]: Current configured display size."""
        return self.__display.get_size()

    @property
    def display(self):
        """Return the active display surface.
        
        Returns:
            pygame.Surface: Active Pygame display surface."""
        return self.__display
