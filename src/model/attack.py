"""Attack competence model.

An attack is an active competence that can damage a target when the target is
within range. The model stores attack metadata, computes damage based on the
effect-zone center, and triggers the associated visual effect through the
animation manager.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
from typing import Tuple
from src.model.competence import Competence

class Attack(Competence):
    """Offensive competence that applies damage to a target.
    
    The attack checks range before applying damage. Damage is strongest at the center
    of the effect zone and weaker on surrounding affected positions.
    
    Attributes:
        target (Unit | None): Optional target associated with the attack.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self, name: str, power: int, effect_zone: Tuple[int, int, int], speed: int, range: Tuple[int, int, int], target=None):
        """Create an attack competence and optionally store a target reference.
        
        Args:
            name (str): Name identifying the asset, unit, competence, or registered resource.
            power (int): Base numeric strength of the competence.
            effect_zone (Tuple[int, int, int]): Tuple defining the area influenced by the competence.
            speed (int): Movement or playback speed value used by the unit or competence.
            range (Tuple[int, int, int]): Tuple defining vertical, horizontal, and diagonal range constraints.
            target: Target unit affected by an attack or competence.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        super().__init__(name, power, effect_zone, speed, range)
        self.__target = target

    @property
    def target(self):
        """Target associated with the attack, if one has been assigned.
        
        Returns:
            Unit | None: Stored target reference.
        
        Side Effects:
            Updates the stored target reference."""
        return self.__target

    @target.setter
    def target(self, target):
        """Target associated with the attack, if one has been assigned.
        
        Args:
            target: Target unit affected by an attack or competence.
        
        Returns:
            Unit | None: Stored target reference.
        
        Side Effects:
            Updates the stored target reference."""
        self.__target = target

    def calcul_degat(self, target_position: Tuple[int, int], center_position: Tuple[int, int]) -> int:
        """Compute damage according to distance from the effect-zone center.
        
        Args:
            target_position (Tuple[int, int]): Target position expressed as an ``(x, y)`` tuple.
            center_position (Tuple[int, int]): Center position of the effect zone as an ``(x, y)`` tuple.
        
        Returns:
            int: Damage value computed for the target position."""
        effect_x = abs(target_position[0] - center_position[0])
        effect_y = abs(target_position[1] - center_position[1])
        if effect_x <= self.effect_zone[0] and effect_y <= self.effect_zone[1]:
            return self.power if effect_x == 0 and effect_y == 0 else int(self.power * 0.4)
        return 0

    def activate(self, user, target, animation_manager):
        """Apply the attack to a target when it is within range.
        
        Args:
            user: Unit that owns or activates the competence.
            target: Target unit affected by an attack or competence.
            animation_manager: AnimationManager coordinating unit animations and effects.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Applies gameplay effects defined by the concrete competence.
        
        Notes:
            Concrete subclasses define whether activation changes health, damage, or visual effects."""
        if self.is_within_range((user.x, user.y), (target.x, target.y)):
            damage = self.calcul_degat((target.x, target.y), (target.x, target.y))
            if damage > 0:
                print(f'[LOG] {user.name} attacks {target.name}, dealing {damage} damage.')
                target.health = damage
                animation_manager.get_effect(target.name).update(target.x, target.y, 'attacks', self.name)

    def __str__(self):
        """Return a concise debug representation of the object.
        
        Returns:
            str: Human-readable debug representation of the instance."""
        return f'Attack -- [Name: {self.name} | Power: {self.power} | Zone: {self.effect_zone} | Range: {self.range}]'
