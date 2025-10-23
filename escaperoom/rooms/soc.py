#utf-8
"""SOC room."""
from escaperoom.rooms.base import Room


class SOCRoom(Room):
    """SOC room."""
    
    def __init__(self):
        super().__init__(name="SOC room")

    def inspect(self, filepath, game_state):
        """Inspect the room's item and return output lines."""
        output = ["[Room SOC] Inspecting the room..."]
        return output