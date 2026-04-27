"""
Model layer for gameplay data and rules.

The model package defines the domain objects used by the turn-based strategy
game. It contains units, players, abilities, defensive actions, offensive
actions, and factory helpers used to construct configured heroes.

Modules:
    attack:
        Defines offensive abilities that can be used against units.

    competence:
        Defines the base abstraction shared by gameplay abilities.

    defense:
        Defines defensive abilities and protection-oriented actions.

    hero_factory:
        Provides predefined hero construction helpers and sprite metadata.

    player:
        Defines the player entity and its controlled units.

    unit:
        Defines the main unit entity used in combat and map interactions.

Public Classes:
    Attack:
        Represents an offensive ability.

    Competence:
        Base abstraction for abilities.

    Defense:
        Represents a defensive ability.

    HeroFactory:
        Creates configured hero units and associated sprite definitions.

    Player:
        Stores player-related state and controlled units.

    Unit:
        Represents a combat unit displayed on the map.
"""

# from .attack import Attack
# from .competence import Competence
# from .defense import Defense
# from .hero_factory import HeroFactory
# from .player import Player
# from .unit import Unit
#
# __all__ = [
#     "Attack",
#     "Competence",
#     "Defense",
#     "HeroFactory",
#     "Player",
#     "Unit",
# ]