"""Unit domain model.

A unit represents a playable hero on the battlefield. It stores combat state,
position, team ownership, available actions, learned competences, and rendering
metadata required by the view layer.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
from typing import Tuple
import pygame
from pygame import Rect
from src.model.attack import Attack
from src.settings import Settings
from src.view.map import Map
GRID_SIZE = 8
CELL_SIZE = 60
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE

class Unit(pygame.sprite.Sprite):
    """Playable battlefield unit.
    
    A unit combines gameplay state such as health, team, movement range, available
    actions, and competences with the position data needed by the animation layer.
    It also provides movement, attack dispatch, defense activation, and state
    synchronization helpers.
    
    Attributes:
        state (str): Current gameplay and animation state.
        actions (dict[str, bool]): Per-turn action availability flags.
        old_position (list[int]): Last saved position used for rollback.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self, name: str, x: int, y: int, health: int, team: str, speed: int, range: Tuple[int, int, int]=(2, 3, 1)):
        """Create a playable unit.
        
        Args:
            name (str): Name identifying the asset, unit, competence, or registered resource.
            x (int): Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y (int): Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            health (int): Value used by the   init   operation.
            team (str): Team or player identifier used to separate allies from enemies.
            speed (int): Movement or playback speed value used by the unit or competence.
            range (Tuple[int, int, int]): Tuple defining vertical, horizontal, and diagonal range constraints.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        super().__init__()
        self.__name = name
        self.__x = x
        self.__y = y
        self.__health = float(health)
        self.__team = team
        self.__speed = speed
        self.__movement_range = range
        self.__is_selected = False
        self.__competences = {'attacks': [], 'defenses': []}
        self.__image = None
        self.state = 'idle'
        self.old_position = [self.__x, self.__y].copy()
        self.actions = {'move': True, 'attack': True, 'defend': True}

    @property
    def name(self):
        """Return the display name.
        
        Returns:
            str: Display name."""
        return self.__name

    @property
    def x(self):
        """Horizontal position in pixels.
        
        Returns:
            int: Current horizontal position in pixels.
        
        Side Effects:
            Updates the internal horizontal coordinate when it remains within bounds."""
        return self.__x

    @x.setter
    def x(self, value):
        """Horizontal position in pixels.
        
        Args:
            value: New value assigned to the property.
        
        Returns:
            int: Current horizontal position in pixels.
        
        Side Effects:
            Updates the internal horizontal coordinate when it remains within bounds."""
        if 0 <= value < SCREEN_WIDTH:
            self.__x = value
        else:
            print(f'Invalid X position: {value}')

    @property
    def y(self):
        """Vertical position in pixels.
        
        Returns:
            int: Current vertical position in pixels.
        
        Side Effects:
            Updates the internal vertical coordinate when it remains within bounds."""
        return self.__y

    @y.setter
    def y(self, value):
        """Vertical position in pixels.
        
        Args:
            value: New value assigned to the property.
        
        Returns:
            int: Current vertical position in pixels.
        
        Side Effects:
            Updates the internal vertical coordinate when it remains within bounds."""
        if 0 <= value < SCREEN_HEIGHT:
            self.__y = value
        else:
            print(f'Invalid Y position: {value}')

    @property
    def health(self):
        """Current health points.
        
        Returns:
            float: Current health points.
        
        Side Effects:
            Reduces health and sets the unit state to dead when health reaches zero."""
        return self.__health

    @health.setter
    def health(self, damage):
        """Current health points.
        
        Args:
            damage: Incoming damage value to transform or apply.
        
        Returns:
            float: Current health points.
        
        Side Effects:
            Reduces health and sets the unit state to dead when health reaches zero."""
        if damage > 0:
            old_health = self.__health
            self.__health = max(0, self.__health - damage)
            print(f'[LOG] {self.name}: Health updated from {old_health:.2f} to {self.__health:.2f}')
            if self.__health <= 0:
                self.state = 'dead'
                print(f'[LOG] {self.name} is now dead.')

    @property
    def team(self):
        """Team or player identifier.
        
        Returns:
            str: Team or player identifier."""
        return self.__team

    @property
    def speed(self):
        """Return the speed value.
        
        Returns:
            int: Configured speed value."""
        return self.__speed

    @property
    def movement_range(self):
        """Movement range limits.
        
        Returns:
            tuple[int, int, int]: Movement range constraints."""
        return self.__movement_range

    @property
    def is_selected(self):
        """Whether the unit is currently selected.
        
        Returns:
            bool: Selection state.
        
        Side Effects:
            Updates the selection flag."""
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, value):
        """Whether the unit is currently selected.
        
        Args:
            value: New value assigned to the property.
        
        Returns:
            bool: Selection state.
        
        Side Effects:
            Updates the selection flag."""
        self.__is_selected = value

    @property
    def competences(self):
        """Competences grouped by category.
        
        Returns:
            dict[str, list]: Competences grouped by category."""
        return self.__competences

    @property
    def image(self):
        """Current image associated with the object.
        
        Returns:
            pygame.Surface | None: Current image surface.
        
        Side Effects:
            Replaces the current image surface."""
        return self.__image

    @image.setter
    def image(self, value):
        """Current image associated with the object.
        
        Args:
            value: New value assigned to the property.
        
        Returns:
            pygame.Surface | None: Current image surface.
        
        Side Effects:
            Replaces the current image surface."""
        self.__image = value

    def add_competence(self, competence, type):
        """Attach an attack or defense competence to the unit.
        
        Args:
            competence: Attack or defense object to attach to the unit.
            type: Action subtype, competence name, or category key used by the caller.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Appends the competence to the attack or defense collection."""
        if type == 'attack':
            self.__competences['attacks'].append(competence)
        elif type == 'defense':
            self.__competences['defenses'].append(competence)
        else:
            print(f'Unknown competence type: {type}')

    def activate_defense(self, damage: int, animation_manager) -> int:
        """Apply all defensive competences to an incoming damage value.
        
        Args:
            damage (int): Incoming damage value to transform or apply.
            animation_manager: AnimationManager coordinating unit animations and effects.
        
        Returns:
            int | float: Damage remaining after every defense has been applied.
        
        Side Effects:
            Triggers each defense effect and logs damage reduction."""
        if self.state == 'dead':
            print(f'{self.name} is already dead and cannot defend.')
            return damage
        for defense in self.__competences['defenses']:
            old_damage = damage
            defense.activate(self, animation_manager)
            damage = defense.reduce_damage(damage, animation_manager, self)
            print(f'[LOG] {self.name}: Damage reduced from {old_damage} to {damage} by {defense.name}.')
        return damage

    def attack(self, target, attack, animation_manager):
        """Dispatch an attack competence against a target unit.
        
        Args:
            target: Target unit affected by an attack or competence.
            attack: Attack competence selected for execution or range testing.
            animation_manager: AnimationManager coordinating unit animations and effects.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            May reduce target health and start the attack effect.
        
        Notes:
            The method delegates damage computation to the selected Attack instance."""
        if self.state == 'dead':
            print(f'{self.name} is dead and cannot attack.')
            return
        if target is None:
            print(f'{self.name} has no target for the attack.')
            return
        if isinstance(attack, Attack):
            attack.activate(self, target, animation_manager)
        else:
            print(f'Invalid competence used by {self.name}.')

    def move(self, dx: int, dy: int, rect: Rect, feet: Rect, map_obj: Map):
        """Move the unit by a pixel offset when the destination remains inside the map.
        
        Args:
            dx (int): Horizontal displacement in pixels.
            dy (int): Vertical displacement in pixels.
            rect (Rect): Sprite rectangle synchronized with the unit position.
            feet (Rect): Collision rectangle representing the unit feet.
            map_obj (Map): Map object used to validate movement bounds.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Saves the previous position, moves the unit, and synchronizes rectangles when valid.
        
        Notes:
            The method validates map bounds but leaves collision resolution to the caller or surrounding game loop."""
        if self.state == 'dead':
            print(f'{self.name} is dead and cannot move.')
            return
        setting = Settings()
        new_x = self.__x + dx
        new_y = self.__y + dy
        if 0 <= new_x + setting.sprite_width / 2 <= map_obj.width and 0 <= new_y + setting.sprite_height / 2 <= map_obj.height:
            self.save_location()
            self.__x = new_x
            self.__y = new_y
            self.update(rect, feet)
        else:
            print(f'Movement impossible for {self.name} ({new_x}, {new_y} out of bounds).')

    def save_location(self):
        """Store the current coordinates so the unit can be restored later.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Stores the current coordinates for later rollback."""
        self.old_position = [self.__x, self.__y].copy()

    def move_back(self, rect: Rect, feet: Rect):
        """Restore the last saved position and synchronize collision rectangles.
        
        Args:
            rect (Rect): Sprite rectangle synchronized with the unit position.
            feet (Rect): Collision rectangle representing the unit feet.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Restores the saved coordinates and synchronizes rectangles."""
        self.__x = self.old_position[0]
        self.__y = self.old_position[1]
        rect.topleft = (self.__x, self.__y)
        feet.midbottom = rect.midbottom
        self.update(rect, feet)

    def update(self, rect: Rect, feet: Rect):
        """Synchronize the unit position with its sprite and feet rectangles.
        
        Args:
            rect (Rect): Sprite rectangle synchronized with the unit position.
            feet (Rect): Collision rectangle representing the unit feet.
        
        Returns:
            bool | None: For animations and effects, indicates completion or active playback; for rendering/update controllers, no explicit value is returned.
        
        Side Effects:
            Mutates animation, effect, terrain, and rendering state depending on the object.
        
        Notes:
            The method is part of the frame loop and is expected to be called repeatedly."""
        rect.topleft = (self.__x, self.__y)
        feet.x = self.__x + rect.width * 0.7 / 4
        feet.y = self.__y + rect.height * 0.75

    def set_state(self, state, action_type, effect, target_pos=None):
        """Update the unit state and optionally trigger a visual effect.
        
        Args:
            state: Gameplay or animation state to apply.
            action_type: Specific action or competence type to associate with the state.
            effect: Effect instance associated with a unit or action.
            target_pos: Optional target position used to place or interpolate a visual effect.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Changes the unit state and may start a visual effect."""
        if self.state != 'dead':
            self.state = state
            if (state == 'attacks' or state == 'defenses') and effect is not None:
                effect.update(self.__x, self.__y, state, action_type, target_pos)

    def reset_movement_range(self):
        """Reset the movement reference position to the current coordinates.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Updates the saved reference position."""
        self.old_position = [self.__x, self.__y].copy()

    def __str__(self):
        """Return a concise debug representation of the object.
        
        Returns:
            str: Human-readable debug representation of the instance."""
        return f'Unit -- [Name: {self.name} | Health: {self.health} | Position: ({self.__x}, {self.__y}) | Team: {self.team}]'
