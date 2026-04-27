"""Defense competence model.

A defense is an active competence that reduces incoming damage by a percentage
stored in its power value. It also triggers the corresponding defensive visual
effect when one is available for the unit.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
from typing import Tuple
from src.model.competence import Competence
from src.model.unit import Unit

class Defense(Competence):
    """Defensive competence that reduces incoming damage.
    
    The defense interprets its power as a percentage reduction and can trigger a
    visual effect on the protected unit.
    
    Attributes:
        power (int): Percentage reduction applied to incoming damage.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self, name: str, power: int, effect_zone: Tuple[int, int, int], speed: int, range: Tuple[int, int, int]):
        """Create a defense competence.
        
        Args:
            name (str): Name identifying the asset, unit, competence, or registered resource.
            power (int): Base numeric strength of the competence.
            effect_zone (Tuple[int, int, int]): Tuple defining the area influenced by the competence.
            speed (int): Movement or playback speed value used by the unit or competence.
            range (Tuple[int, int, int]): Tuple defining vertical, horizontal, and diagonal range constraints.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        super().__init__(name, power, effect_zone, speed, range)

    def reduce_damage(self, damage, animation_manager, user):
        """Reduce an incoming damage value and trigger the defense effect.
        
        Args:
            damage: Incoming damage value to transform or apply.
            animation_manager: AnimationManager coordinating unit animations and effects.
            user: Unit that owns or activates the competence.
        
        Returns:
            object: Value produced by the underlying game or rendering operation.
        
        Side Effects:
            Triggers defensive feedback and returns the reduced damage value."""
        reduction = self.power / 100 * damage
        final_damage = max(0, damage - reduction)
        print(f'[LOG] {user.name} reduces damage by {reduction:.2f} with {self.name}.')
        effect = animation_manager.get_effect(user.name)
        if effect:
            effect.update(user.x, user.y, 'defenses', self.name)
        else:
            print(f'[LOG] No animation found for {user.name}. Defense: {self.name}')
        return final_damage

    def activate(self, user: Unit, animation_manager):
        """Trigger the defense activation feedback for the protected unit.
        
        Args:
            user (Unit): Unit that owns or activates the competence.
            animation_manager: AnimationManager coordinating unit animations and effects.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Applies gameplay effects defined by the concrete competence.
        
        Notes:
            Concrete subclasses define whether activation changes health, damage, or visual effects."""
        print(f'[LOG] {user.name} activates {self.name}. Current health: {user.health}')
        effect = animation_manager.get_effect(user.name)
        if effect:
            effect.update(user.x, user.y, 'defenses', self.name)
        else:
            print(f'[LOG] No animation found for {user.name}. Defense: {self.name}')

    def __str__(self):
        """Return a concise debug representation of the object.
        
        Returns:
            str: Human-readable debug representation of the instance."""
        return f'Defense -- [Name: {self.name} | Power: {self.power}% | Zone: {self.effect_zone} | Range: {self.range}]'
