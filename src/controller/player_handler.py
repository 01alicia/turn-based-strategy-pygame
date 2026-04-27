"""Player input controller for in-game actions.

The player handler translates keyboard state and key-down events into movement,
attack, and defense actions for the active unit. It also resolves attack targets,
updates animation state, and notifies the game loop when a turn may be complete.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
import pygame
from src.controller.animation_manager import AnimationManager
from src.model.unit import Unit
from src.view.map import Map

class PlayerHandler:
    """Controller for the currently active unit.
    
    A ``PlayerHandler`` is created around the unit whose turn is active. It converts
    keyboard input into movement, attack, and defense commands while preserving the
    turn rules stored on the unit action flags.
    
    Attributes:
        name (str): Name of the active unit.
        animation_manager (AnimationManager): Registry used for animations, effects, and units.
        map (Map): Map used for movement constraints.
        game (Game): Game loop object receiving turn updates.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self, player: Unit, animation_manager: AnimationManager, map: Map, game):
        """Bind input handling to the active unit, map, animation manager, and game.
        
        Args:
            player (Unit): Active Unit controlled by the input handler.
            animation_manager (AnimationManager): AnimationManager coordinating unit animations and effects.
            map (Map): Map file name or path to load.
            game: Game object receiving turn and state updates.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.name = player.name
        self.animation_manager = animation_manager
        self.map = map
        self.game = game

    @property
    def player(self):
        """Return the active unit controlled by this handler.
        
        Returns:
            Unit: Active unit resolved from the animation manager registry."""
        return self.animation_manager.heros[self.name]

    def get_effect(self, type):
        """Return the first competence effect of the requested type, if available.
        
        Args:
            type: Action subtype, competence name, or category key used by the caller.
        
        Returns:
            Effect | None: Registered effect matching the requested key, if available."""
        if type in self.animation_manager.effects:
            return self.animation_manager.effects[type]
        return None

    def key_pressed_event(self):
        """Apply continuous keyboard movement for the active unit.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Moves the active unit, changes unit state, and updates orientation or animation."""
        if self.game.text_info is None:
            self.game.text_info = ''
        if self.player.state == 'dead':
            self.animation_manager.update_animation(self.player, 'dead', 'dead')
            return
        pressed = pygame.key.get_pressed()
        anim = self.animation_manager.get_animation(self.name)
        effect = self.animation_manager.get_effect(self.name)
        if effect is not None and effect.current_effect is None:
            move_distance = self.player.speed
            if pressed[pygame.K_LEFT]:
                self.player.move(-move_distance, 0, anim.rect, anim.feet, self.map)
                self.player.set_state('movement', 'side', None)
                self.animation_manager.update_animation(self.player, 'movement', 'side')
                self.animation_manager.set_orientation(self.name, 'left')
            elif pressed[pygame.K_RIGHT]:
                self.player.move(move_distance, 0, anim.rect, anim.feet, self.map)
                self.player.set_state('movement', 'side', None)
                self.animation_manager.update_animation(self.player, 'movement', 'side')
                self.animation_manager.set_orientation(self.name, 'right')
            elif pressed[pygame.K_UP]:
                self.player.move(0, -move_distance, anim.rect, anim.feet, self.map)
                self.player.set_state('movement', 'up-down', None)
                self.animation_manager.update_animation(self.player, 'movement', 'up-down')
            elif pressed[pygame.K_DOWN]:
                self.player.move(0, move_distance, anim.rect, anim.feet, self.map)
                self.player.set_state('movement', 'up-down', None)
                self.animation_manager.update_animation(self.player, 'movement', 'up-down')
            else:
                self.player.set_state('idle', 'idle', None)
                self.animation_manager.update_animation(self.player, 'idle', 'idle')

    def find_target(self, attack):
        """Find the first enemy unit that is within range of the given attack.
        
        Args:
            attack: Attack competence selected for execution or range testing.
        
        Returns:
            Unit | None: First living enemy unit inside the attack range, or ``None``."""
        user_position = (self.player.x, self.player.y)
        for unit in self.animation_manager.heros.values():
            if unit.team != self.player.team and unit.state != 'dead':
                target_position = (unit.x, unit.y)
                if attack.is_within_range(user_position, target_position):
                    self.game.text_info += f'Target found : {unit.name} at {target_position} position\n'
                    print(f'Target found: {unit.name} at position {target_position}')
                    return unit
        print('No valid target found.')
        return None

    def key_down_event(self, event, screen, dt):
        """Handle one-shot keyboard actions such as attacks, defenses, and turn updates.
        
        Args:
            event: Pygame event to process.
            screen: Pygame surface or screen wrapper used as the drawing target.
            dt: Elapsed time since the previous frame, used to advance animations.
        
        Returns:
            object: Value produced by the underlying game or rendering operation.
        
        Side Effects:
            Executes attacks or defenses, updates action flags, and may advance turns.
        
        Notes:
            Only discrete key presses are handled here; continuous movement is handled separately."""
        if self.player.state == 'dead':
            self.game.text_info += self.game.current_unit.name + " is dead and can't act!\n"
            print(f'{self.player.name} is dead and cannot act.')
            self.animation_manager.heros[self.name].set_state('dead', 'dead', self.animation_manager.get_effect(self.animation_manager.heros[self.name].name), None)
            self.animation_manager.update_animation(self.player, 'dead', 'dead')
            self.game.check_end_of_turn()
            self.game.check_game_over()
            return
        if (event.key == pygame.K_a or event.key == pygame.K_b) and self.player.actions['defend']:
            if self.player.competences['defenses']:
                if event.key == pygame.K_a:
                    defense = self.player.competences['defenses'][0]
                else:
                    defense = self.player.competences['defenses'][1]
                self.animation_manager.heros[self.name].set_state('defenses', defense.name, self.animation_manager.get_effect(self.name), (self.player.x, self.player.y))
                self.game.text_info += f"{self.player.name} activates '{defense.name}' defense\n"
                print(f'{self.player.name} activates defense: {defense.name}')
                damage = 50
                reduced_damage = self.player.activate_defense(damage, self.animation_manager)
                print(f'Damage after defense: {reduced_damage}')
                self.game.text_info += f'Damage after defense activation {reduced_damage}\n'
                self.animation_manager.update_animation(self.player, 'defenses', defense.name)
                self.player.actions['defend'] = False
                self.game.check_end_of_turn()
                self.game.check_game_over()
            return None
        if (event.key == pygame.K_c or event.key == pygame.K_v) and self.player.actions['attack']:
            attack_index = 0 if event.key == pygame.K_c else 1
            if attack_index < len(self.player.competences['attacks']):
                target_pos = None
                attack = self.player.competences['attacks'][attack_index]
                target = self.find_target(attack)
                if target is not None:
                    target_pos = (target.x, target.y)
                self.animation_manager.heros[self.name].set_state('attacks', attack.name, self.animation_manager.get_effect(self.animation_manager.heros[self.name].name), target_pos)
                if target:
                    self.game.text_info += f"{self.player.name} activates '{attack.name}' attack on {target.name}\n"
                    print(f'{self.player.name} uses attack: {attack.name} on {target.name}.')
                    self.player.attack(target, attack, self.animation_manager)
                else:
                    self.game.text_info += f"No target found for '{attack.name}' attack\n"
                    print(f'No valid target found for attack {attack.name}.')
                self.animation_manager.update_animation(self.player, 'attacks', attack.name)
                self.player.actions['attack'] = False
                self.game.check_end_of_turn()
                self.game.check_game_over()
            self.game.text_info += f"A: {self.player.competences['defenses'][0]} \nB: {self.player.competences['defenses'][1]} \n"
