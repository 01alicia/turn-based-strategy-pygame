"""Runtime orchestration for the turn-based strategy game.

This module defines the central ``Game`` singleton. It coordinates player setup,
unit creation, the active turn, input dispatch, map updates, animations, visual
effects, and game-over detection. The module is intended to remain the top-level
entry point and therefore keeps references to the controller, model, and view
layers.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
from src.controller.animation_manager import AnimationManager
from src.controller.menu_handler import MenuHandler
from src.controller.player_handler import PlayerHandler
from src.model.hero_factory import HeroFactory
from src.model.player import Player
from src.settings import SingletonMeta, Settings
from src.view.animation_factory import AnimationFactory
from src.view.map import Map
from src.view.screen import Screen

class Game(metaclass=SingletonMeta):
    """Central runtime object that coordinates the full game session.
    
    The game owns the active screen, map, clock, animation registry, players, and
    turn indexes. It is responsible for creating entities from the menu selection,
    running the main event loop, updating the world, drawing the frame, and deciding
    when the match is over.
    
    The object is intentionally stateful: it owns the current player, current unit, selected heroes, map, and rendering helpers for the whole session.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self):
        """Create the game state and instantiate shared runtime components.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.is_running = False
        self.players = {}
        self.screen = Screen()
        self.map = Map(self.screen)
        self.clock = pygame.time.Clock()
        self.animation_manager = AnimationManager()
        self.animation_factory = AnimationFactory()
        self.settings = Settings()
        self.current_player_index = 0
        self.current_unit_index = 0
        self.players_list = []
        self.current_player = None
        self.current_unit = None
        self.text_info = None

    def initialize_entities(self, selected_units):
        """Create players, units, animations, and effects from menu selections.
        
        Args:
            selected_units: Mapping of player names to the hero names selected during the menu flow.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Creates players, heroes, animations, and effects used by the game loop."""
        if selected_units:
            for i, (name, unit_names) in enumerate(selected_units.items()):
                player = Player(name)
                for j, unit_name in enumerate(unit_names):
                    unit, sprite_conf = HeroFactory.create_hero(unit_name, self.settings.team_indexes[i][j][0], self.settings.team_indexes[i][j][1], name)
                    if unit:
                        unit.actions = {'move': True, 'attack': True, 'defend': True}
                        player.units[unit_name] = unit
                        self.animation_manager.add_hero(unit)
                        self.animation_manager.add_animation(unit.name, self.animation_factory.create_animation(unit, sprite_conf))
                        self.animation_manager.add_effect(unit.name, self.animation_factory.create_effect(sprite_conf))
                        self.animation_manager.set_orientation(unit.name, 'right')
                self.players[name] = player
            self.players_list = list(self.players.keys())
            self.current_player = self.players[self.players_list[self.current_player_index]]
            self.current_unit = list(self.current_player.units.values())[self.current_unit_index]
            self.reset_unit_actions()

    def reset_unit_actions(self):
        """Restore the current unit's turn actions.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Resets action flags on the current unit."""
        if self.current_unit:
            self.current_unit.actions = {'move': True, 'attack': True, 'defend': True}
            print(f'Actions reset for {self.current_unit.name}.')
            self.text_info = f"C: '{self.current_unit.competences['attacks'][0]}' \nV: '{self.current_unit.competences['attacks'][1]}' \n"

    def next_unit(self):
        """Advance the turn to the next living unit.
        
        If the current player has no remaining unit in the current scan order, control is
        passed to the next eligible player.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Changes the current unit and may advance to the next player."""
        while True:
            self.current_unit_index += 1
            if self.current_unit_index >= len(self.current_player.units):
                self.current_unit_index = 0
                self.next_player()
                return
            self.current_unit = list(self.current_player.units.values())[self.current_unit_index]
            if self.current_unit.state != 'dead':
                print(f'Switching to next unit: {self.current_unit.name}.')
                self.reset_unit_actions()
                break

    def next_player(self):
        """Advance the turn to the next player with at least one living unit.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Changes the current player and resets the active unit selection."""
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players_list)
            self.current_player = self.players[self.players_list[self.current_player_index]]
            if any((unit.state != 'dead' for unit in self.current_player.units.values())):
                self.current_unit_index = 0
                self.current_unit = list(self.current_player.units.values())[self.current_unit_index]
                print(f'Switching to next player: {self.current_player.name}.')
                self.reset_unit_actions()
                break
            if self.check_game_over():
                return

    def check_game_over(self):
        """Return whether the match has ended.
        
        Returns:
            bool: ``True`` when the match has ended; otherwise ``False``.
        
        Side Effects:
            May remove defeated players from the game state."""
        for player_name, player in self.players.items():
            if all((unit.state == 'dead' for unit in player.units.values())):
                print(f'Player {player_name} has lost all units.')
                self.players_list.remove(player_name)
                if len(self.players_list) == 1:
                    print(f'Player {self.players_list[0]} has won the game!')
                    self.is_running = False
                    rect = pygame.draw.rect(self.screen.display, (0, 0, 0, 128), pygame.Rect(0, 0, self.settings.screen_width, self.settings.screen_height))
                    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 128))
                    self.screen.display.blit(overlay, (rect.x, rect.y))
                    font = pygame.font.Font(f'{Settings().path}/assets/EagleLake-Regular.ttf', 20)
                    text_surface = font.render(f'Game Over {player_name}!', True, (255, 255, 255))
                    self.screen.display.blit(text_surface, (500, 300))
                    pygame.display.flip()
                    time.sleep(20)
                    return True
        return False

    def check_end_of_turn(self):
        """Move to the next unit when the active unit has finished its turn.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            May advance the turn when the active unit has exhausted its actions."""
        if self.current_unit.state == 'dead':
            print(f'{self.current_unit.name} is dead. Skipping turn.')
            self.next_unit()
            return
        if not self.current_unit.actions['attack'] and (not self.current_unit.actions['defend']):
            print(f'{self.current_unit.name} has completed its turn.')
            self.next_unit()

    def update(self):
        """Update unit animations, terrain interactions, collisions, and map rendering state.
        
        Returns:
            bool | None: For animations and effects, indicates completion or active playback; for rendering/update controllers, no explicit value is returned.
        
        Side Effects:
            Mutates animation, effect, terrain, and rendering state depending on the object.
        
        Notes:
            The method is part of the frame loop and is expected to be called repeatedly."""
        for player in self.players.values():
            for unit in player.units.values():
                anim = self.animation_manager.get_animation(unit.name)
                if anim:
                    if anim.feet.collidelist(self.map.collisions) > -1:
                        unit.move_back(anim.rect, anim.feet)
                    if anim.feet.collidelist(self.map.lava_tiles) > -1:
                        if unit.name != 'Natsu':
                            unit.health = 0
                            unit.set_state('dead', None, None)
                    if unit.name != 'Gray' and anim.feet.collidelist(self.map.ice_tiles) > -1:
                        unit.move_back(anim.rect, anim.feet)
                    if unit.state == 'dead':
                        anim.state = 'dead'
                        anim.type = 'dead'
                    anim.update(self.clock.get_time(), self.animation_manager.orientation[unit.name])
                if unit.state != 'dead':
                    if anim.feet.collidelist(self.map.collisions) > -1:
                        unit.move_back(anim.rect, anim.feet)
        self.map.group.update()
        self.map.update(self.animation_manager, self.current_unit)

    def run(self, avatars, avatar_names, info_box, info_box_0):
        """Run the main gameplay loop.
        
        Args:
            avatars: Avatar rectangles or UI elements returned by the menu layer.
            avatar_names: Display names associated with the player avatars.
            info_box: Primary rectangle used to display turn and action information.
            info_box_0: Secondary rectangle used to display additional contextual information.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Processes events, updates game state, draws frames, and may terminate the game loop."""
        self.is_running = True
        while self.is_running:
            self.screen.display.fill((0, 0, 0))
            dt = self.clock.tick(60) / 1000
            handler = PlayerHandler(self.current_unit, self.animation_manager, self.map, self)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:
                        self.is_running = False
                    handler.key_down_event(event, self.screen.display, dt)
            handler.key_pressed_event()
            self.update()
            avatar_names = list(self.current_player.units.keys())
            self.draw(avatars, avatar_names, info_box, info_box_0)

    def draw(self, avatar_rects, avatar_names, info_box, info_box_0):
        """Draw the current frame, including effects, map, units, avatars, and turn panels.
        
        Args:
            avatar_rects: Avatar rectangles used to render player portraits.
            avatar_names: Display names associated with the player avatars.
            info_box: Primary rectangle used to display turn and action information.
            info_box_0: Secondary rectangle used to display additional contextual information.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Blits animation and effect frames to the target surface."""
        selected_avatar = self.current_unit.name
        animation = self.animation_manager.get_animation(self.current_unit.name)
        effect = self.animation_manager.get_effect(self.current_unit.name)
        for player in self.players.values():
            for unit in player.units.values():
                animation = self.animation_manager.get_animation(unit.name)
                effect = self.animation_manager.get_effect(unit.name)
                if effect and effect.current_effect is not None:
                    if not effect.apply_effect(self.clock.get_time(), self.animation_manager.orientation[unit.name]):
                        print(f'Effect completed for {unit.name}.')
                        effect.current_effect = None
                    effect.draw(self.screen.display)
        self.map.update(self.animation_manager, self.current_unit)
        if effect and effect.current_effect is not None:
            effect.draw(self.screen.display)
        for i, rect in enumerate(avatar_rects):
            self.screen.display.blit(pygame.image.load(f'{Settings().path}/assets/ui/{avatar_names[i]}_hud.png'), rect)
            if selected_avatar == avatar_names[i]:
                self.current_unit.is_selected = True
                self.screen.display.blit(pygame.image.load(f'{Settings().path}/assets/ui/selected_hud.png'), avatar_rects[i])
        pygame.draw.rect(self.screen.display, (50, 50, 50), info_box)
        pygame.draw.rect(self.screen.display, (200, 200, 200), info_box, 2)
        pygame.draw.rect(self.screen.display, (50, 50, 50), info_box_0)
        pygame.draw.rect(self.screen.display, (200, 200, 200), info_box_0, 2)
        turn_info = f"Player: {self.current_player.name} | Unit: {self.current_unit.name} | Actions: Move - {self.current_unit.actions['move']}, Attack - {self.current_unit.actions['attack']}, Defend - {self.current_unit.actions['defend']}"
        turn_text = pygame.font.Font(f'{Settings().path}/assets/EagleLake-Regular.ttf', 20).render(turn_info, True, (255, 255, 255))
        self.screen.display.blit(turn_text, (10, 10))
        self.draw_multiline_text(info_box, pygame.font.Font(f'{Settings().path}/assets/EagleLake-Regular.ttf', 20), (255, 255, 255))
        self.draw_multiline_text(info_box_0, pygame.font.Font(f'{Settings().path}/assets/EagleLake-Regular.ttf', 20), (255, 255, 255), f'{self.current_unit.team} \n {self.current_unit.name} \n {self.current_unit.health}')
        pygame.display.flip()

    def start(self):
        """Run the menu flow, initialize the selected entities, and launch the game loop.
        
        Returns:
            object: The value produced by the menu or game loop, when one is returned by the underlying flow.
        
        Side Effects:
            Runs menu or game loops and may initialize runtime state."""
        pygame.init()
        icon = pygame.image.load(f'{Settings().path}/assets/ui/icon.png')
        banner = pygame.image.load(f'{Settings().path}/assets/ui/banner.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Strategy Game')
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        # WINDOW_MARGIN = 40
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        banner = pygame.transform.scale(banner, screen.get_size())
        SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
        DISPLAY_WIDTH = min(1200, SCREEN_WIDTH)
        DISPLAY_START_Y = SCREEN_HEIGHT - 250
        AVATAR_SIZE = 120
        INFO_BOX_HEIGHT = SCREEN_HEIGHT - (DISPLAY_START_Y + AVATAR_SIZE + 20)
        AVATAR_SPACING = 20
        start_x = (SCREEN_WIDTH - DISPLAY_WIDTH) // 2
        menu_handler = MenuHandler()
        menu_handler.menu(False, banner, self.clock, screen)
        self.initialize_entities(menu_handler.selected_units)
        avatar_names = list(self.current_player.units.keys())
        info_start_y = DISPLAY_START_Y + AVATAR_SIZE + 20
        info_box_0 = pygame.Rect(DISPLAY_WIDTH / 2 + 10, info_start_y - INFO_BOX_HEIGHT - 10, DISPLAY_WIDTH / 2 - 10, INFO_BOX_HEIGHT)
        info_box = pygame.Rect(start_x, info_start_y, DISPLAY_WIDTH, INFO_BOX_HEIGHT)
        avatars = []
        for i in range(3):
            avatar = pygame.Rect(start_x + i * (AVATAR_SIZE + AVATAR_SPACING), DISPLAY_START_Y, AVATAR_SIZE, AVATAR_SIZE)
            avatars.append(avatar)
        self.run(avatars, avatar_names, info_box, info_box_0)
        self.update()
        self.draw(avatars, avatar_names, info_box, info_box_0)
        pygame.display.flip()
        pygame.quit()

    def draw_multiline_text(self, info_box, font, color, text=None):
        """Render multiline text inside an information box.
        
        Args:
            info_box: Primary rectangle used to display turn and action information.
            font: Font object used to render text.
            color: Text color passed to Pygame rendering APIs.
            text: Multiline text content to render.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Renders text lines onto the provided information box."""
        max_lines = 4
        if text is None:
            text = self.text_info
        lines = text.split('\n')
        x, y = (info_box.x + 5, info_box.y + 5)
        line_spacing = font.get_linesize()
        display = []
        for line in lines:
            display.append(line)
            if len(display) > max_lines:
                display.pop(0)
        for i in range(len(display)):
            text_surface = font.render(display[i], True, color)
            self.screen.display.blit(text_surface, (x, y))
            y += line_spacing
if __name__ == '__main__':
    game = Game()
    game.start()
