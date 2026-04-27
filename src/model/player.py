"""Player domain model.

A player owns a collection of units and tracks the currently selected unit and
attack. The class intentionally contains only player state; input handling and
turn management are performed by controller and game-loop classes.

The documentation follows Google-style docstrings so tools such as pdoc, Sphinx Napoleon,
or MkDocs-based pipelines can expose parameters, return values, and side effects in a
consistent HTML API reference."""

class Player:
    """Container for the units controlled by one player.
    
    The class keeps the player's name, units, selected unit, and selected attack. It
    does not implement input or turn logic directly.
    
    This model is a lightweight container and does not implement combat or rendering behavior directly.
    
    Notes:
        This class is documented as part of the public project API and is intended to be readable in generated HTML documentation."""

    def __init__(self, name):
        """Create an empty player state for the given name.
        
        Args:
            name: Name identifying the asset, unit, competence, or registered resource.
        
        Side Effects:
            Initializes instance attributes and keeps references to shared runtime objects."""
        self.name = name
        self.units = {}
        self.selected_unit = None
        self.selected_attack = None

    def select_unit(self):
        """Store the unit currently marked as selected, if any.
        
        Returns:
            None: This method is executed for its side effects."""
        if self.units is not None:
            for unit in self.units.values():
                if unit.is_selected:
                    self.selected_unit = unit

    def __str__(self):
        """Return a concise debug representation of the object.
        
        Returns:
            str: Human-readable debug representation of the instance."""
        return f'Player -- [Name: {self.name} | Units: {self.units}]'
