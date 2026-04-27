"""Factory for predefined hero units and their sprite configurations.

The factory centralizes all playable hero definitions. Each hero method creates a
``Unit`` with its combat competences, while ``sprite_config`` defines how the
corresponding sprite sheet must be indexed for idle, movement, attack, defense,
effect, and death animations.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""
from src.model.attack import Attack
from src.model.defense import Defense
from src.model.unit import Unit
from src.view.sprites_config import SpriteConfig

class HeroFactory:
    """Factory for constructing predefined hero units.
    
    Each hero method returns a fully configured ``Unit`` with its attacks and
    defenses. The factory also exposes sprite configuration data so the rendering
    layer knows which frames belong to each unit state and competence.
    
    The factory centralizes hero statistics, competences, and sprite metadata so the rest of the project can request heroes by name without duplicating setup data.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    @staticmethod
    def sprite_config(name):
        """Return sprite frame indexes and effect metadata for a hero name.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        if name == 'Erza':
            return SpriteConfig({'idle': [6, 7]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [14, 6, 7]}, {'Sword of destiny': [4, 5, 6, 7], 'Titania attack': [8, 9, 10, 11, 22, 14]}, {'Fairy aura': [0, 1, 2, 3], 'Diamond shield': [6, 7]}, {'Titania attack': (5, 6, True, 190), 'Diamond shield': (5, 5, False, 190), 'Fairy aura': (5, 4, False, 190), 'Sword of destiny': (5, 2, True, 120)}, {'dead': [15]})
        if name == 'Gray':
            return SpriteConfig({'idle': [6, 7]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [22, 6, 7]}, {'Frozen swords': [14, 4, 5, 6], 'Icy destruction': [8, 9, 10, 11, 22, 14]}, {'Ice shield': [7, 8, 9, 10], 'Absolute ice': [6, 7]}, {'Icy destruction': (5, 5, True, 190), 'Frozen swords': (5, 4, True, 190), 'Absolute ice': (5, 2, False, 190)}, {'dead': [15]})
        if name == 'Natsu':
            return SpriteConfig({'idle': [6, 7]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [22, 6, 7]}, {"Fire dragon's iron fist": [14, 4, 5], "Fire dragon's roar": [8, 9, 10, 14]}, {'Protective flame': [0, 1, 2, 3], 'Flame envelope': [6, 7]}, {"Fire dragon's iron fist": (5, 3, True, 190), "Fire dragon's roar": (5, 2, True, 180), 'Flame envelope': (5, 5, False, 190)}, {'dead': [15]})
        if name == 'Kansuke':
            return SpriteConfig({'idle': [0, 1, 2, 3]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [22, 13, 14]}, {'Infinite light': [4, 5, 6, 7], 'Holy light': [8, 22, 9, 10]}, {'Dissipative clarity': [0, 1, 2, 3], 'Protective ray': [0, 1, 2, 3]}, {'Holy light': (5, 5, True, 190), 'Protective ray': (5, 4, False, 190), 'Infinite light': (5, 6, True, 190), 'Dissipative clarity': (5, 6, False, 190)}, {'dead': [15]})
        if name == 'Gowther':
            return SpriteConfig({'idle': [0, 1, 2, 3]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [22, 14]}, {'Darkness flare bomb': [8, 9, 10], 'Obscurity tentacles': [0, 1, 2, 3]}, {'Shadow rune shield': [3, 4, 5], 'Demon aura': [0, 1, 2, 3]}, {'Darkness flare bomb': (5, 5, True, 190), 'Shadow rune shield': (5, 6, False, 190), 'Obscurity tentacles': (5, 5, True, 190), 'Demon aura': (5, 6, False, 190)}, {'dead': [15]})
        if name == 'Heisuke':
            return SpriteConfig({'idle': [0, 1, 2, 3]}, {'side': [16, 17, 18, 19, 20, 21], 'up-down': [22, 14]}, {'Thunderball': [14, 4, 5], 'Lightning saber': [8, 9, 10]}, {'Regenerative lightning': [0, 1, 2, 3, 14], 'Lightning strike': [0, 1, 2, 3]}, {'Thunderball': (5, 2, True, 190), 'Lightning saber': (5, 3, True, 190), 'Regenerative lightning': (3, 1, False, 190), 'Lightning strike': (5, 6, False, 190)}, {'dead': [15]})

    @staticmethod
    def erza(x, y, team):
        """Create the Erza hero with sword-based attacks and defensive aura skills.
        
        Args:
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            team: Team or player identifier used to separate allies from enemies.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        erza = Unit('Erza', x, y, 100, team, 10)
        erza.add_competence(Attack('Sword of destiny', 80, (150, 120, 0), 10, (150, 250, 145), None), 'attack')
        erza.add_competence(Attack('Titania attack', 75, (100, 150, 0), 10, (260, 340, 130), None), 'attack')
        erza.add_competence(Defense('Fairy aura', 20, (100, 100, 0), 10, (0, 0, 0)), 'defense')
        erza.add_competence(Defense('Diamond shield', 35, (200, 100, 0), 10, (0, 0, 0)), 'defense')
        sprite_conf = HeroFactory.sprite_config(erza.name)
        return (erza, sprite_conf)

    @staticmethod
    def gray(x, y, team):
        """Create the Gray hero with ice-based attacks and defensive skills.
        
        Args:
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            team: Team or player identifier used to separate allies from enemies.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        gray = Unit('Gray', x, y, 100, team, 10)
        gray.add_competence(Attack('Frozen swords', 80, (120, 220, 0), 10, (285, 145, 135), None), 'attack')
        gray.add_competence(Attack('Icy destruction', 70, (130, 120, 0), 10, (250, 180, 140), None), 'attack')
        gray.add_competence(Defense('Ice shield', 15, (100, 100, 0), 10, (0, 0, 0)), 'defense')
        gray.add_competence(Defense('Absolute ice', 30, (200, 200, 0), 10, (0, 0, 0)), 'defense')
        sprite_conf = HeroFactory.sprite_config(gray.name)
        return (gray, sprite_conf)

    @staticmethod
    def natsu(x, y, team):
        """Create the Natsu hero with fire-based attacks and defensive skills.
        
        Args:
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            team: Team or player identifier used to separate allies from enemies.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        natsu = Unit('Natsu', x, y, 130, team, 10)
        natsu.add_competence(Attack("Fire dragon's iron fist", 85, (330, 230, 0), 10, (160, 260, 170), None), 'attack')
        natsu.add_competence(Attack("Fire dragon's roar", 70, (250, 130, 0), 10, (170, 250, 145), None), 'attack')
        natsu.add_competence(Defense('Protective flame', 30, (100, 100, 0), 10, (0, 0, 0)), 'defense')
        natsu.add_competence(Defense('Flame envelope', 20, (200, 100, 0), 10, (0, 0, 0)), 'defense')
        sprite_conf = HeroFactory.sprite_config(natsu.name)
        return (natsu, sprite_conf)

    @staticmethod
    def kansuke(x, y, team):
        """Create the Kansuke hero with sword techniques and defensive skills.
        
        Args:
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            team: Team or player identifier used to separate allies from enemies.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        kansuke = Unit('Kansuke', x, y, 100, team, 10)
        kansuke.add_competence(Attack('Infinite light', 85, (140, 240, 0), 10, (255, 255, 145), None), 'attack')
        kansuke.add_competence(Attack('Holy light', 75, (300, 300, 0), 10, (260, 260, 150), None), 'attack')
        kansuke.add_competence(Defense('Dissipative clarity', 20, (100, 100, 0), 10, (0, 0, 0)), 'defense')
        kansuke.add_competence(Defense('Protective ray', 35, (200, 200, 0), 10, (0, 0, 0)), 'defense')
        sprite_conf = HeroFactory.sprite_config(kansuke.name)
        return (kansuke, sprite_conf)

    @staticmethod
    def gowther(x, y, team):
        """Create the Gowther hero with ranged magical attacks and barriers.
        
        Args:
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            team: Team or player identifier used to separate allies from enemies.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        gowther = Unit('Gowther', x, y, 120, team, 10)
        gowther.add_competence(Attack('Darkness flare bomb', 80, (153, 130, 0), 10, (140, 150, 180), None), 'attack')
        gowther.add_competence(Attack('Obscurity tentacles', 60, (220, 250, 0), 10, (165, 160, 150), None), 'attack')
        gowther.add_competence(Defense('Shadow rune shield', 35, (100, 100, 0), 10, (0, 0, 0)), 'defense')
        gowther.add_competence(Defense('Demon aura', 20, (250, 250, 0), 10, (0, 0, 0)), 'defense')
        sprite_conf = HeroFactory.sprite_config(gowther.name)
        return (gowther, sprite_conf)

    @staticmethod
    def heisuke(x, y, team):
        """Create the Heisuke hero with sword techniques and defensive skills.
        
        Args:
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            team: Team or player identifier used to separate allies from enemies.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        heisuke = Unit('Heisuke', x, y, 140, team, 10)
        heisuke.add_competence(Attack('Thunderball', 75, (240, 140, 0), 10, (165, 155, 145), None), 'attack')
        heisuke.add_competence(Attack('Lightning saber', 60, (230, 300, 0), 10, (270, 260, 250), None), 'attack')
        heisuke.add_competence(Defense('Regenerative lightning', 15, (110, 110, 0), 10, (0, 0, 0)), 'defense')
        heisuke.add_competence(Defense('Lightning strike', 10, (320, 200, 0), 10, (0, 0, 0)), 'defense')
        sprite_conf = HeroFactory.sprite_config(heisuke.name)
        return (heisuke, sprite_conf)

    @staticmethod
    def create_hero(name, x, y, team):
        """Create a hero and its sprite configuration from a hero name.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
            x: Horizontal coordinate in pixels, unless explicitly used as a grid coordinate.
            y: Vertical coordinate in pixels, unless explicitly used as a grid coordinate.
            team: Team or player identifier used to separate allies from enemies.
        
        Returns:
            object: Value produced by the underlying game or rendering operation."""
        if name == 'Erza':
            return HeroFactory.erza(x, y, team)
        elif name == 'Gray':
            return HeroFactory.gray(x, y, team)
        elif name == 'Natsu':
            return HeroFactory.natsu(x, y, team)
        elif name == 'Heisuke':
            return HeroFactory.heisuke(x, y, team)
        elif name == 'Kansuke':
            return HeroFactory.kansuke(x, y, team)
        elif name == 'Gowther':
            return HeroFactory.gowther(x, y, team)
