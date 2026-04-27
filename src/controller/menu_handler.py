"""Menu input controller for player setup and configuration screens.

This module handles low-level Pygame events for the start menu, player-name
entry, hero selection, and display settings. It stores the temporary selection
state that is later consumed by the main game initialization.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
import math
import pygame
from src.settings import Settings

class MenuHandler:
    """Stateful controller for menu interactions.
    
    The handler receives Pygame events from the menu view and updates temporary menu
    state such as the current player name, selected heroes, and selected marker
    positions. Once two valid teams have been selected, it returns the selection data
    used to initialize the game.
    
    Attributes:
        selected_units (dict[str, list[str]]): Hero selections grouped by player.
        player_names (list[str]): Names entered by players.
        current_player (int): Index of the player currently being configured.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self):
        """Initialize menu selection state.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.current_player = None
        self.set_player = True
        self.selected_units = {}
        self.settings = Settings()
        self.x, self.y = ([], [])
        pass

    def select_units(self, event, erza_rect, gray_rect, natsu_rect, gowther_rect, kansuke_rect, heisuke_rect):
        """Handle mouse-based hero selection for the current player.
        
        The method toggles a hero in the current player's selection and stores the
        coordinates used to draw the selection marker.
        
        Args:
            event: Pygame event to process.
            erza_rect: Clickable rectangle associated with the Erza hero button.
            gray_rect: Clickable rectangle associated with the Gray hero button.
            natsu_rect: Clickable rectangle associated with the Natsu hero button.
            gowther_rect: Clickable rectangle associated with the Gowther hero button.
            kansuke_rect: Clickable rectangle associated with the Kansuke hero button.
            heisuke_rect: Clickable rectangle associated with the Heisuke hero button.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Updates the current player selection and menu state."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected = None
            x, y = (None, None)
            if erza_rect.collidepoint(event.pos):
                selected = 'Erza'
                x, y = (erza_rect.x + erza_rect.w / 2 - 20, erza_rect.y + erza_rect.h - 25)
            elif gray_rect.collidepoint(event.pos):
                selected = 'Gray'
                x, y = (gray_rect.x + gray_rect.w / 2 - 20, gray_rect.y + gray_rect.h - 25)
            elif natsu_rect.collidepoint(event.pos):
                selected = 'Natsu'
                x, y = (natsu_rect.x + natsu_rect.w / 2 - 20, natsu_rect.y + natsu_rect.h - 25)
            elif gowther_rect.collidepoint(event.pos):
                selected = 'Gowther'
                x, y = (gowther_rect.x + gowther_rect.w / 2 - 20, gowther_rect.y + gowther_rect.h - 25)
            elif kansuke_rect.collidepoint(event.pos):
                selected = 'Kansuke'
                x, y = (kansuke_rect.x + kansuke_rect.w / 2 - 20, kansuke_rect.y + kansuke_rect.h - 25)
            elif heisuke_rect.collidepoint(event.pos):
                selected = 'Heisuke'
                x, y = (heisuke_rect.x + heisuke_rect.w / 2 - 20, heisuke_rect.y + heisuke_rect.h - 25)
            if selected is not None:
                if self.current_player in self.selected_units:
                    if not selected in self.selected_units[self.current_player]:
                        if len(self.selected_units[self.current_player]) < self.settings.nb_units_per_player:
                            self.selected_units[self.current_player].append(selected)
                            if x is not None and y is not None:
                                self.x.append(x)
                                self.y.append(y)
                    else:
                        self.selected_units[self.current_player].remove(selected)
                        if x is not None and y is not None:
                            if x in self.x:
                                self.x.remove(x)
                            if y in self.y:
                                self.y.remove(y)
                else:
                    print('Please enter a username first.')

    def get_player_name(self, event, input_rect, text, active):
        """Handle text input for the current player name.
        
        Args:
            event: Pygame event to process.
            input_rect: Text input rectangle used for player-name editing.
            text: Multiline text content to render.
            active: Whether the text input currently has keyboard focus.
        
        Returns:
            tuple[str, bool]: Updated text value and focus state.
        
        Side Effects:
            Processes input focus and text content for player names."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            active = input_rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and active and self.set_player:
            if event.key == pygame.K_RETURN:
                self.current_player = text
                if not self.current_player in self.selected_units:
                    self.selected_units[self.current_player] = []
                    self.set_player = False
                else:
                    print('Name is already in use.')
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode
        return (text, active)

    def submit(self, event, ok_rect):
        """Validate the current selection when the confirmation button is pressed.
        
        Args:
            event: Pygame event to process.
            ok_rect: Clickable rectangle used to confirm the current selection.
        
        Returns:
            bool | None: Submission status when the confirmation action is processed.
        
        Side Effects:
            Validates selection state and advances menu progression when valid."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ok_rect.collidepoint(event.pos):
                all_three_selected = all((len(units) == 3 for units in self.selected_units.values()))
                if len(self.selected_units) == 2 and all_three_selected:
                    self.set_player = False
                    self.x, self.y = ([], [])
                    return 'end'
                if len(self.selected_units) == 1 and all_three_selected:
                    self.set_player = True
                    print(len(self.selected_units) == 1, all_three_selected)
                    self.x, self.y = ([], [])
                    return ''
                self.set_player = True
        return None

    def start(self, clock):
        """Run the menu loop and return the selected units once setup is complete.
        
        Args:
            clock: Pygame clock used to regulate the menu loop.
        
        Returns:
            object: The value produced by the menu or game loop, when one is returned by the underlying flow.
        
        Side Effects:
            Runs menu or game loops and may initialize runtime state."""
        pygame.init()
        pressed = False
        icon = pygame.image.load('../../assets/ui/icon.png')
        banner = pygame.image.load('../../assets/ui/banner.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Strategy Game')
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        banner = pygame.transform.scale(banner, screen.get_size())
        self.menu(pressed, banner, clock, screen)
        pygame.quit()

    def menu(self, pressed, banner, clock, screen):
        """Handle events and screen transitions on the main menu.
        
        Args:
            pressed: Current keyboard state returned by Pygame.
            banner: Menu banner surface or rectangle used by the menu screen.
            clock: Pygame clock used to regulate the menu loop.
            screen: Pygame surface or screen wrapper used as the drawing target.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Handles menu events, screen transitions, and display refresh."""
        is_running = True
        try:
            play_button, play_button_rect = self.settings.create_ui_element('play_button', (250, 100), math.ceil(screen.get_width() / 2.5), math.ceil(screen.get_height() / 3))
            settings_button, settings_button_rect = self.settings.create_ui_element('settings_button', (250, 100), math.ceil(screen.get_width() / 2.5), play_button_rect.y + 10)
            settings_button_rect.y += settings_button_rect.height
            exit_button, exit_button_rect = self.settings.create_ui_element('exit_button', (250, 100), math.ceil(screen.get_width() / 2.5), settings_button_rect.y + settings_button_rect.height + 10)
        except pygame.error as e:
            print(f'Error loading button image: {e}')
            return
        while is_running:
            screen.blit(banner, (0, 0))
            if not pressed:
                screen.blit(play_button, play_button_rect)
                screen.blit(settings_button, settings_button_rect)
                screen.blit(exit_button, exit_button_rect)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        self.choose_player(screen, banner)
                        is_running = False
                    elif settings_button_rect.collidepoint(event.pos):
                        print('Settings button pressed.')
                    elif exit_button_rect.collidepoint(event.pos):
                        is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:
                        is_running = False
            pygame.display.flip()
            clock.tick(60)

    def choose_player(self, screen, banner):
        """Handle player naming and unit selection events on the team selection screen.
        
        Args:
            screen: Pygame surface or screen wrapper used as the drawing target.
            banner: Menu banner surface or rectangle used by the menu screen.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Processes player naming, hero selection, and confirmation events."""
        is_running = True
        active = False
        font = pygame.font.Font(f'{Settings().path}/assets/EagleLake-Regular.ttf', 30)
        text = ''
        try:
            input_button = pygame.image.load(f'{Settings().path}/assets/ui/input.png')
            input_button = pygame.transform.scale(input_button, (400, 150))
            input_rect = input_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
            placeholder, placeholder_rect = self.settings.create_ui_element('placeholder', (400, 45), input_rect.x, input_rect.y - 10)
            erza_avatar, erza_rect = self.settings.create_ui_element('erza_avatar', (200, 300), 80, input_rect.y + input_rect.height + 10)
            gray_avatar, gray_rect = self.settings.create_ui_element('gray_avatar', (200, 300), 320, input_rect.y + input_rect.height + 10)
            natsu_avatar, natsu_rect = self.settings.create_ui_element('natsu_avatar', (200, 300), 560, input_rect.y + input_rect.height + 10)
            gowther_avatar, gowther_rect = self.settings.create_ui_element('gowther_avatar', (200, 300), 800, input_rect.y + input_rect.height + 10)
            heisuke_avatar, heisuke_rect = self.settings.create_ui_element('heisuke_avatar', (200, 300), 1040, input_rect.y + input_rect.height + 10)
            kansuke_avatar, kansuke_rect = self.settings.create_ui_element('kansuke_avatar', (200, 300), 1280, input_rect.y + input_rect.height + 10)
            ok_button = pygame.image.load(f'{Settings().path}/assets/ui/ok_button.png')
            ok_button = pygame.transform.scale(ok_button, (200, 75))
            ok_rect = ok_button.get_rect(center=(screen.get_width() / 2, 3 * screen.get_height() / 4))
        except pygame.error as e:
            print(f'Error loading button image: {e}')
            return
        clock = pygame.time.Clock()
        while is_running:
            screen.blit(banner, (0, 0))
            screen.blit(input_button, input_rect)
            screen.blit(placeholder, placeholder_rect)
            overlay_color = (0, 255, 0, 128) if active else (255, 0, 0, 128)
            overlay_surface = pygame.Surface((input_rect.width - 40, input_rect.height - 80), pygame.SRCALPHA)
            overlay_surface.fill(overlay_color)
            overlay_x = input_rect.x + 20
            overlay_y = input_rect.y + 40
            screen.blit(overlay_surface, (overlay_x, overlay_y))
            screen.blit(erza_avatar, erza_rect)
            screen.blit(gray_avatar, gray_rect)
            screen.blit(natsu_avatar, natsu_rect)
            screen.blit(gowther_avatar, gowther_rect)
            screen.blit(heisuke_avatar, heisuke_rect)
            screen.blit(kansuke_avatar, kansuke_rect)
            screen.blit(ok_button, ok_rect)
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (overlay_x, overlay_y))
            for x, y in zip(self.x, self.y):
                screen.blit(pygame.image.load(f'{Settings().path}/assets/ui/selected.png'), (x, y))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_END:
                        is_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = input_rect.collidepoint(event.pos)
                self.select_units(event, erza_rect, gray_rect, natsu_rect, gowther_rect, kansuke_rect, heisuke_rect)
                text, active = self.get_player_name(event, input_rect, text, active)
                new_text = self.submit(event, ok_rect)
                if new_text is not None:
                    if new_text != 'end':
                        text = new_text
                    else:
                        is_running = False
            pygame.display.flip()
            clock.tick(60)

    def display_settings(self):
        """Handle events on the settings screen.
        
        Returns:
            None: This method is executed for its side effects.
        
        Side Effects:
            Applies settings-screen events and may update display resolution."""
        pass
