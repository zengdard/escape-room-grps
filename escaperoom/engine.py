"""REPL loop + GameState + command routing."""

import json
import os
from escaperoom.transcript import TranscriptLogger
from escaperoom.rooms.soc import SOCRoom
from escaperoom.rooms.dns import DNSRoom
from escaperoom.rooms.vault import VaultRoom
from escaperoom.rooms.malware import MalwareRoom
from escaperoom.utils import verify_hmac, compute_hmac


class GameState:
    """Manages the game state."""
    
    def __init__(self):
        self.current_room = "intro"
        self.inventory = {}
        self.tokens = {}
        self.evidence = {}
    

class GameEngine:
    """Main game engine with REPL loop."""
    
    def __init__(self, starting_room="intro", transcript_file="run.txt", data_dir="msc-group-03"):
        self.state = GameState()
        self.state.current_room = starting_room
        self.transcript = TranscriptLogger(transcript_file)
        self.running = False
        self.data_dir = data_dir
        
        # Initialize rooms
        self.rooms = {
            "intro": {"description": "Intro Lobby", "exits": ["soc", "dns", "vault", "malware", "final"], "items": []},
            "soc": {"description": "SOC Triage Desk", "exits": ["intro", "dns", "vault", "malware", "final"], "items": ["auth.log"], "handler": SOCRoom()},
            "dns": {"description": "DNS Closet", "exits": ["intro", "soc", "vault", "malware", "final"], "items": ["dns.cfg"], "handler": DNSRoom()},
            "vault": {"description": "Vault Corridor", "exits": ["intro", "soc", "dns", "malware", "final"], "items": ["vault_dump.txt"], "handler": VaultRoom()},
            "malware": {"description": "Malware Lab", "exits": ["intro", "soc", "dns", "vault", "final"], "items": ["proc_tree.jsonl"], "handler": MalwareRoom()},
            "final": {"description": "Final Gate", "exits": ["intro", "soc", "dns", "vault", "malware"], "items": ["gate"]}
        }
    
    def run(self):
        """Start the REPL loop."""
        self.running = True
        output = "[Game] Cyber Escape Room started. Type 'help' for commands."
        print(output)
        self.transcript.log_output(output)
        
        while self.running:
            try:
                command = input("> ").strip()
                if command:
                    self.transcript.log_command(command)
                    self.process_command(command)
            except (KeyboardInterrupt, EOFError):
                print()
                self.quit_game()
                break
    
    def output(self, message):
        """Print and log output."""
        print(message)
        self.transcript.log_output(message)
    
    def process_command(self, command):
        """Route commands to appropriate handlers."""
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in ["exit", "quit"]:
            self.quit_game()
        elif cmd == "help":
            self.show_help()
        elif cmd == "look":
            self.look()
        elif cmd == "move":
            self.move(args)
        elif cmd == "inspect":
            self.inspect(args)
        elif cmd == "use":
            self.use_item(args)
        elif cmd == "inventory":
            self.show_inventory()
        elif cmd == "hint":
            self.show_hint()
        elif cmd == "save":
            self.save_game(args)
        elif cmd == "load":
            self.load_game(args)
        else:
            self.output(f"Unknown command: {cmd}")
    
    def quit_game(self):
        """Quit the game."""
        self.running = False
        self.output(f"[Game] Goodbye. Transcript written to {self.transcript.filename}")
    
    def show_help(self):
        """Show available commands."""
        self.output("Commands: look, move <room>, inspect <item>, use <item>, inventory, hint, save, load, quit")
    
    def look(self):
        """Look around the current room."""
        room = self.rooms.get(self.state.current_room)
        if not room:
            return None
        
        if self.state.current_room == "intro":
            self.output("You are in the Intro Lobby.")
            self.output("A terminal blinks in the corner. Doors lead to: soc, dns, vault, malware, final.")
        elif self.state.current_room == "soc":
            self.output("You enter the SOC Triage Desk.")
            self.output("A cluttered screen shows failed SSH login attempts.")
            self.output("Items here: auth.log")
        elif self.state.current_room == "dns":
            self.output("You enter the DNS Closet.")
            self.output("The walls are covered with scribbled key=value pairs.")
            self.output("Items here: dns.cfg")
        elif self.state.current_room == "vault":
            self.output("You enter the Vault Corridor.")
            self.output("The safe looms before you, covered in scratches and codes.")
            self.output("Items here: vault_dump.txt")
        elif self.state.current_room == "malware":
            self.output("You enter the Malware Lab.")
            self.output("Process trees sprawl across multiple screens.")
            self.output("Items here: proc_tree.jsonl")
        elif self.state.current_room == "final":
            self.output("You stand before the Final Gate. The console asks for proof.")
    
    def move(self, room_name):
        """Move to another room."""
        if not room_name:
            self.output("Move where?")
            return
        
        current = self.rooms.get(self.state.current_room)
        if room_name not in current.get("exits", []):
            self.output(f"Cannot move to {room_name} from here.")
            return
        
        self.state.current_room = room_name
        self.look()
    
    def inspect(self, item_name):
        """Inspect an item in the current room."""
        if not item_name:
            self.output("Inspect what?")
            return
        
        room = self.rooms.get(self.state.current_room)
        if item_name not in room.get("items", []):
            self.output(f"{item_name} not found here.")
            return
        
        # Delegate to room handler
        handler = room.get("handler")
        if handler:
            filepath = os.path.join(self.data_dir, item_name)
            result = handler.inspect(filepath, self.state)
            if result:
                for line in result:
                    self.output(line)
    
    def use_item(self, item_name):
        """Use an item from inventory or in room."""
        if item_name == "gate" and self.state.current_room == "final":
            self.check_final_gate()
        else:
            self.output(f"Cannot use {item_name}")
    
    def check_final_gate(self):
        """Check if all tokens are collected and verify against final_gate.txt."""
        # Parse final_gate.txt
        gate_file = os.path.join(self.data_dir, "final_gate.txt")
        
        try:
            with open(gate_file, 'r', encoding='utf-8') as f:
                gate_config = {}
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        gate_config[key.strip()] = value.strip()
        except FileNotFoundError:
            self.output("[Final Gate] Error: final_gate.txt not found")
            return
        
        token_order = gate_config.get('token_order', '').split(',')
        token_order = [t.strip() for t in token_order]
        group_id = gate_config.get('group_id', '')
        expected_hmac = gate_config.get('expected_hmac', '')
        
        # Collect tokens
        collected = {k: self.state.tokens.get(k, "?") for k in token_order}
        
        status = ", ".join([f"{k}={v}" for k, v in collected.items()])
        self.output(f"Collected tokens: {status}")
        
        if all(v != "?" for v in collected.values()):
            # Build message according to token_order
            token_values = [self.state.tokens[k] for k in token_order]
            token_str = "-".join(token_values)
            message = f"{group_id}|{token_str}"
            
            self.output("All tokens found! Verifying...")
            self.output(f"MSG={message}")
            
            # Compute HMAC
            computed_hmac = compute_hmac(group_id, message, digestmod='sha256')
            self.output(f"COMPUTED_HMAC={computed_hmac}")
            self.output(f"EXPECTED_HMAC={expected_hmac}")
            
            # Verify HMAC
            if verify_hmac(group_id, message, expected_hmac, digestmod='sha256'):
                self.output("✓ HMAC VERIFIED! The gate opens...")
                self.output("[Final Gate] SUCCESS - All flags verified correctly!")
            else:
                self.output("✗ HMAC VERIFICATION FAILED!")
                self.output("[Final Gate] The gate remains locked. Check your tokens.")
        else:
            self.output("Not all tokens found. The gate remains locked.")
    
    def show_inventory(self):
        """Show inventory."""
        if self.state.inventory:
            items = ", ".join(self.state.inventory.keys())
            self.output(f"You currently hold: {items}")
        else:
            self.output("Your inventory is empty.")
    
    def show_hint(self):
        """Show a hint for the current room."""
        hints = {
            "soc": "Parse the log file line by line. Look for Failed password entries.",
            "dns": "Check the token_tag to know which hint to decode.",
            "vault": "Find SAFE{a-b-c} where a+b=c",
            "malware": "Build a process tree and find the malicious chain."
        }
        hint = hints.get(self.state.current_room, "No hints available here.")
        self.output(f"[Hint] {hint}")
    
    def save_game(self, filename):
        """Save game state."""
        if not filename:
            filename = "save.json"
        
        save_data = {
            "current_room": self.state.current_room,
            "inventory": self.state.inventory,
            "tokens": self.state.tokens,
            "evidence": self.state.evidence
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        self.output(f"[Game] Progress saved.")
    
    def load_game(self, filename):
        """Load game state."""
        if not filename:
            filename = "save.json"
        
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            self.state.current_room = save_data.get("current_room", "intro")
            self.state.inventory = save_data.get("inventory", {})
            self.state.tokens = save_data.get("tokens", {})
            self.state.evidence = save_data.get("evidence", {})
            
            self.output(f"[Game] Progress loaded.")
        except FileNotFoundError:
            self.output(f"[Game] Save file not found.")

