# utf-8
"""DNS room logic: parse `dns.cfg`, normalize lines, and decode Base64 hints."""

import re
import base64
from escaperoom.rooms.base import Room


class DNSRoom(Room):
    """ DNS room with Base64 hint decoding."""

    def __init__(self):
        super().__init__(name="DNS room")
        # Precompile regex for key=value hints
        self.hint_line = re.compile(r'([a-zA-Z0-9_]+)\s*=\s*(.+)')

    def try_base64_decode(self, i: str):
        """Safely decode Base64, return string or None."""
        i = "".join(i.split())
        try:
            text = base64.b64decode(i, validate=True).decode("utf-8")
        except Exception:
            return None
        return text if sum(32 <= ord(c) <= 126 for c in text) / max(1, len(text)) >= 0.5 else None

    def inspect(self, filepath, game_state):
        """ Parse dns.cfg and find valid DNS token hints."""
        output = ["[Room DNS] Searching for DNS hints..."]

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            return ["[Room DNS] Error: dns.cfg not found"]

        # Normalize lines with backslash continuation
        lines, buf = [], ""
        for line in content.splitlines():
            line = line.rstrip()
            buf += line[:-1] if line.endswith('\\') else line
            if not line.endswith('\\'):
                lines.append(buf)
                buf = ""

        # Find all key=value pairs
        pairs = [(m.group(1), m.group(2)) for l in lines if (m := self.hint_line.search(l))]
        if not pairs:
            return output + ["No DNS hint lines found."]

        # Decode Base64 values
        decoded_hints = {k: (v, dec) for k, v in pairs if (dec:= self.try_base64_decode(v))}
        if not decoded_hints:
            return output + ["No valid Base64 hints decoded."]

        # Pick token_tag if present, else first English-like hint
        chosen_key, chosen_enc, chosen_dec = None, None, None
        if "token_tag" in decoded_hints:
            chosen_key, (chosen_enc, chosen_dec) = "token_tag", decoded_hints["token_tag"]
        else:
            for k, (enc, dec) in decoded_hints.items():
                if len(dec.split()) >= 2:
                    chosen_key, chosen_enc, chosen_dec = k, enc, dec
                    break

        if not chosen_key:
            return output + ["No hint text contains a valid token clue."]

        # Update game state
        game_state.tokens["DNS"] = chosen_dec
        game_state.inventory["DNS"] = True

        # Output
        output += [
            f"Found valid DNS hint: {chosen_key}={chosen_enc}",
            f"TOKEN[DNS]={chosen_dec}",
            f'EVIDENCE[DNS].MATCH="{chosen_key}={chosen_enc}"',
            f"EVIDENCE[DNS].CHECK={chosen_key}→decoded({chosen_dec})"
        ]
        return output
