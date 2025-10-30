"""Vault room logic: parse `vault_dump.txt` and locate SAFE{a-b-c} where a+b=c."""

import re
from escaperoom.rooms.base import Room


class VaultRoom(Room):
    """Vault Corridor room."""
    
    def __init__(self):
        super().__init__(name="Vault room")
        # Precompile regex for SAFE{a-b-c} pattern
        self.safe_pattern = re.compile(r'SAFE\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\}', re.IGNORECASE)
    
    def inspect(self, filepath, game_state):
        """Parse vault_dump.txt and find valid SAFE code."""
        output = ["[Room Vault] Searching for safe codes..."]
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            return ["[Room Vault] Error: vault_dump.txt not found"]
        
        # Find all SAFE{a-b-c} candidates
        matches = self.safe_pattern.findall(content)
        
        valid_code = None
        for match in matches:
            a, b, c = int(match[0]), int(match[1]), int(match[2])
            if a + b == c:
                valid_code = f"{a}-{b}-{c}"
                match_str = f"SAFE{{{a}-{b}-{c}}}"
                
                # Update game state
                game_state.tokens["SAFE"] = valid_code
                game_state.inventory["SAFE"] = True
                
                output.append(f"Found valid code: {match_str}")
                output.append(f"TOKEN[SAFE]={valid_code}")
                output.append(f'EVIDENCE[SAFE].MATCH="{match_str}"')
                output.append(f"EVIDENCE[SAFE].CHECK={a}+{b}={c}")
                break
        
        if not valid_code:
            output.append("No valid SAFE code found (none satisfy a+b=c)")
        
        return output

