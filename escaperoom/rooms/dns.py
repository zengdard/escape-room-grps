#utf-8
"""DNS room."""
from escaperoom.rooms.base import Room


class DNSRoom(Room):
    """DNS room."""
    
    def __init__(self):
        super().__init__(name="DNS room")

    def inspect(self, filepath, game_state):
        """Inspect the room's item and return output lines."""
        output = ["[Room DNS] Inspecting the room..."]
        return output