"""Abstract base class defining the room interface and common state."""

from abc import ABC, abstractmethod


class Room(ABC):
    """Abstract base class for all rooms."""
    
    def __init__(self, name):
        self.name = name
        self.solved = False
    
    @abstractmethod
    def inspect(self, filepath, game_state):
        """Inspect the room's item and return output lines."""
        pass

