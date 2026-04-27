"""Abstract competence model shared by attacks and defenses.

A competence represents an action available to a unit. It defines common metadata
such as name, power, effect zone, activation speed, and range, while leaving the
activation behavior to concrete subclasses.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
from abc import ABC, abstractmethod
from typing import Tuple

class Competence(ABC):
    """Abstract base class for all unit competences.
    
    A competence describes an action that has a power value, an effect zone, an
    activation speed, and a range. Subclasses provide the concrete activation logic
    for offensive or defensive behavior.
    
    Attributes:
        name (str): Display name.
        power (int): Base strength value.
        effect_zone (tuple[int, int, int]): Effect-zone constraints.
        speed (int): Activation or animation speed.
        range (tuple[int, int, int]): Range constraints.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self, name: str, power: int, effect_zone: Tuple[int, int, int], speed: int, range: Tuple[int, int, int]):
        """Initialize shared competence metadata.
        
        Args:
            name (str): Name identifying the asset, unit, competence, or registered resource.
            power (int): Base numeric strength of the competence.
            effect_zone (Tuple[int, int, int]): Tuple defining the area influenced by the competence.
            speed (int): Movement or playback speed value used by the unit or competence.
            range (Tuple[int, int, int]): Tuple defining vertical, horizontal, and diagonal range constraints.
        
        Raises:
            ValueError: Raised when provided gameplay configuration values are invalid.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        if power < 0 or any((dim < 0 for dim in effect_zone + range)) or speed <= 0:
            raise ValueError('Power, effect-zone, range, and speed values must be positive.')
        self.__name = name
        self.__power = power
        self.__effect_zone = effect_zone
        self.__speed = speed
        self.__range = range

    @property
    def name(self):
        """Return the display name.
        
        Returns:
            str: Display name."""
        return self.__name

    @property
    def power(self):
        """Return the configured power value.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        return self.__power

    @property
    def effect_zone(self):
        """Return the configured effect zone.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        return self.__effect_zone

    @property
    def speed(self):
        """Return the speed value.
        
        Returns:
            int: Configured speed value."""
        return self.__speed

    @property
    def range(self):
        """Return the configured range limits.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        return self.__range

    def is_within_range(self, user_position: Tuple[int, int], target_position: Tuple[int, int]) -> bool:
        """Check whether a target position is inside the competence range.
        
        Args:
            user_position (Tuple[int, int]): Source position expressed as an ``(x, y)`` tuple.
            target_position (Tuple[int, int]): Target position expressed as an ``(x, y)`` tuple.
        
        Returns:
            bool: ``True`` when the target satisfies the competence range constraints."""
        distance_x = abs(target_position[0] - user_position[0])
        distance_y = abs(target_position[1] - user_position[1])
        diagonal_distance = max(distance_x, distance_y)
        in_range = distance_x <= self.range[0] and distance_y <= self.range[1] and (diagonal_distance <= self.range[2])
        print(f'[LOG] Range check: X={distance_x}, Y={distance_y}, Diagonal={diagonal_distance}, Result={in_range}')
        return in_range

    @abstractmethod
    def activate(self, user, target):
        """Activate the competence.
        
        Subclasses must implement the concrete gameplay behavior.
        
        Args:
            user: Unit that owns or activates the competence.
            target: Target unit affected by an attack or competence.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Applies gameplay effects defined by the concrete competence.
        
        Notes:
            Concrete subclasses define whether activation changes health, damage, or visual effects."""
        pass

    def __str__(self):
        """Return a concise debug representation of the object.
        
        Returns:
            str: Human-readable debug representation of the instance."""
        return f'Competence -- [Name: {self.name} | Power: {self.power} | Zone: {self.effect_zone} | Speed: {self.speed} | Range: {self.range}]'
