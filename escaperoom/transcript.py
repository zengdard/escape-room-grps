"""Transcript logger that writes timestamped game I/O into `run.txt`."""

from datetime import datetime


class TranscriptLogger:
    """Logs game transcript to run.txt."""
    
    def __init__(self, filename="run.txt"):
        self.filename = filename
    
    def log_command(self, command):
        """Log a command to the transcript."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] > {command}\n")
    
    def log_output(self, output):
        """Log output to the transcript."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {output}\n")

