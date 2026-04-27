"""Factory helpers for animation-related view objects.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
from src.model.unit import Unit
from src.settings import Settings
from src.view.animation import Animation
from src.view.effect import Effect

class AnimationFactory:
    """Small factory that creates animation and effect view objects.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self):
        """Store shared settings used to create view objects.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.settings = Settings()

    def create_animation(self, hero: Unit, sprite_conf):
        """Create the animation view object associated with a unit.
        
        Args:
            hero (Unit): Unit model instance to register or update.
            sprite_conf: SpriteConfig instance describing frame indexes and effect metadata.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        return Animation(hero.name, hero.x, hero.y, self.settings.sprite_width, self.settings.sprite_height, self.settings.animation_speed, sprite_conf)

    def create_effect(self, sprite_conf):
        """Create the effect view object associated with a sprite configuration.
        
        Args:
            sprite_conf: SpriteConfig instance describing frame indexes and effect metadata.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        return Effect(sprite_conf, self.settings.effect_speed)
