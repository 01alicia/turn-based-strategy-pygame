"""Animation coordination layer.

The animation manager keeps the association between model units, their rendered
animations, their visual effects, and their current facing direction. Controllers
and game-loop code use this registry to update or draw units without directly
managing individual sprite objects.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
from src.model.unit import Unit
from src.view.animation import Animation
from src.view.effect import Effect
from src.view.sprites_config import SpriteConfig

class AnimationManager:
    """Registry that synchronizes units, animations, effects, and orientation.
    
    The manager is used as the bridge between gameplay state and rendered state. It
    stores one animation and, optionally, one effect per unit name. It also records
    which direction each unit is facing so sprite flipping remains consistent across
    movement, attacks, and defenses.
    
    Attributes:
        animations (dict[str, Animation]): Registered unit animations.
        effects (dict[str, Effect]): Registered visual effects.
        heros (dict[str, Unit]): Registered hero models by name.
        orientations (dict[str, str]): Last known rendering orientation by unit name.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self):
        """Initialize empty animation, effect, orientation, and hero registries.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.animations = {}
        self.effects = {}
        self.orientation = {}
        self.sprite_configurations = {}
        self.heros = {}

    def set_orientation(self, name, orientation):
        """Store a unit orientation.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
            orientation: Rendering orientation, typically right or left for mirrored sprites.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Updates the stored orientation for a registered unit."""
        if not name in self.orientation or self.orientation[name] != orientation:
            if orientation == 'right' or orientation == 'left':
                self.orientation[name] = orientation
            else:
                self.orientation[name] = 'right'
                print('Orientation must be "right" or "left".')

    def add_animation(self, name, animation: Animation):
        """Register an animation for a unit name when none exists yet.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
            animation (Animation): Animation instance associated with a unit.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Adds an animation to the registry when the key is not already present."""
        if name not in self.animations:
            self.animations[name] = animation

    def add_hero(self, hero: Unit):
        """Register a hero model instance by unit name.
        
        Args:
            hero (Unit): Unit model instance to register or update.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Adds or replaces a unit in the hero registry."""
        if hero.name not in self.heros:
            self.heros[hero.name] = hero

    def add_effect(self, name, effect: Effect):
        """Register a visual effect object for a unit name when none exists yet.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
            effect (Effect): Effect instance associated with a unit or action.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Adds an effect to the registry when the key is not already present."""
        if name not in self.effects:
            self.effects[name] = effect

    def add_sprite_conf(self, name, sprite_conf: SpriteConfig):
        """Register sprite configuration data for a unit name.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
            sprite_conf (SpriteConfig): SpriteConfig instance describing frame indexes and effect metadata.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Adds sprite metadata to the registry."""
        if name not in self.sprite_configurations:
            self.sprite_configurations[name] = sprite_conf

    def get_animation(self, name) -> Animation:
        """Return the animation registered for a unit name, if present.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
        
        Returns:
            Animation | None: Registered animation for the unit name, if available."""
        if name in self.animations:
            return self.animations[name]

    def get_effect(self, name):
        """Return the effect registered for a unit name, if present.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
        
        Returns:
            Effect | None: Registered effect matching the requested key, if available."""
        if name in self.effects:
            return self.effects[name]
        return None

    def draw(self, screen):
        """Draw all registered unit animations and active effects on the target surface.
        
        Args:
            screen: Pygame surface or screen wrapper used as the drawing target.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Blits animation and effect frames to the target surface."""
        for name, animation in self.animations.items():
            screen.blit(animation.image, (animation.x, animation.y))
        for name, effect in self.effects.items():
            effect.draw(screen)

    def update_animation(self, hero, state, type):
        """Synchronize a unit animation with the latest model state and action type.
        
        Args:
            hero: Unit model instance to register or update.
            state: Gameplay or animation state to apply.
            type: Action subtype, competence name, or category key used by the caller.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Updates animation state and frame selection for one unit."""
        if hero.name in self.heros:
            self.animations[hero.name].x = hero.x
            self.animations[hero.name].y = hero.y
            self.animations[hero.name].type = type
            self.animations[hero.name].state = state

    def update(self, hero, state, type, dt, screen):
        """Update the selected unit animation and its active effect for one frame.
        
        Args:
            hero: Unit model instance to register or update.
            state: Gameplay or animation state to apply.
            type: Action subtype, competence name, or category key used by the caller.
            dt: Elapsed time since the previous frame, used to advance animations.
            screen: Pygame surface or screen wrapper used as the drawing target.
        
        Returns:
            bool | None: For animations and effects, indicates completion or active playback; for rendering/update controllers, no explicit value is returned.
        
        Side Effects:
            Mutates animation, effect, terrain, and rendering state depending on the object.
        
        Notes:
            The method is part of the frame loop and is expected to be called repeatedly."""
        self.update_animation(hero, state, type)
        animation = self.get_animation(hero.name)
        effect = self.get_effect(hero.name)
        if not animation:
            print(f'[DEBUG] No animation component found for {hero.name}.')
            return
        animation.update(dt, self.orientation.get(hero.name, 'right'))
        if effect is not None and effect.current_effect is not None:
            effect.apply_effect(dt, self.orientation.get(hero.name, 'right'))
