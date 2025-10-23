#!/usr/bin/env python3
"""CLI entry point for the escape room game."""

import argparse
from escaperoom.engine import GameEngine


def main():
    """Start the escape room game."""
    parser = argparse.ArgumentParser(description="Cyber Escape Room")
    parser.add_argument("--start", default="intro", help="Starting room (default: intro)")
    parser.add_argument("--transcript", default="run.txt", help="Transcript file (default: run.txt)")
    parser.add_argument("--data", default="msc-group-03", help="Data directory (default: msc-group-03)")
    
    args = parser.parse_args()
    
    engine = GameEngine(starting_room=args.start, transcript_file=args.transcript, data_dir=args.data)
    engine.run()


if __name__ == "__main__":
    main()

