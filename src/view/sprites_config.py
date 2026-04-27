"""Sprite indexing configuration.

``SpriteConfig`` stores the frame indexes and external effect metadata used by
animations and effects. It separates sprite-sheet layout data from gameplay and
rendering logic.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
from src.settings import SingletonMeta

class SpriteConfig:
    """Container for animation frame indexes and effect metadata.
    
    Attributes:
        idle (dict): Idle frame indexes.
        movement (dict): Movement frame indexes.
        attacks (dict): Attack frame indexes.
        defenses (dict): Defense frame indexes.
        effects (dict): Effect metadata.
        dead (dict): Dead-state frame indexes.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self, idle, movement, attacks, defenses, effects, dead):
        """Store frame indexes and effect metadata for a unit sprite sheet.
        
        Args:
            idle: Frame indexes used for the idle animation state.
            movement: Frame indexes used for movement animations.
            attacks: Frame indexes used for attack animations.
            defenses: Frame indexes used for defense animations.
            effects: Metadata describing external visual effects.
            dead: Frame indexes used for the dead animation state.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.idle = idle
        self.movement = movement
        self.attacks = attacks
        self.defenses = defenses
        self.effects = effects
        self.dead = dead

    def get_indexes(self, state):
        """Return frame indexes for a unit animation state.
        
        Args:
            state: Gameplay or animation state to apply.
        
        Returns:
            dict | list | None: Frame indexes associated with the requested state."""
        if state == 'idle':
            return self.idle
        elif state == 'movement':
            return self.movement
        elif state == 'attacks':
            return self.attacks
        elif state == 'defenses':
            return self.defenses
        elif state == 'dead':
            return self.dead

    def get_effects(self, type):
        """Return effect metadata for a competence type.
        
        Args:
            type: Action subtype, competence name, or category key used by the caller.
        
        Returns:
            dict | tuple | None: Effect metadata associated with the requested type."""
        if type in self.effects.keys():
            return self.effects[type]
        return None
