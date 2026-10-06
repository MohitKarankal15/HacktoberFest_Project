"""
AI Short-Term Memory for GEMMA WORLD
Stores a FIFO ring buffer of recent events and computes situational trends.
"""
import time
from config import MAX_RECENT_EVENTS

class AIMemory:
    def __init__(self, max_events=MAX_RECENT_EVENTS):
        self.max_events = max_events
        self.events = []  # [{"event": str, "timestamp": float}]

    def record(self, event_str):
        """Adds event with high-resolution timestamp."""
        self.events.append({
            "event": event_str,
            "timestamp": time.time()
        })
        if len(self.events) > self.max_events:
            self.events.pop(0)

    def get_recent_event_strings(self):
        """Returns list of event strings."""
        return [item["event"] for item in self.events]

    def get_summary(self):
        """Computes summary heuristics of recent events."""
        recent_strings = [item["event"].lower() for item in self.events]
        deaths = sum(1 for e in recent_strings if "died" in e or "pit" in e)
        enemies_beaten = sum(1 for e in recent_strings if "defeated" in e)
        damage_taken = sum(1 for e in recent_strings if "lost health" in e or "shield" in e)
        
        return {
            "recent_deaths": deaths,
            "recent_defeats": enemies_beaten,
            "recent_damage_instances": damage_taken,
            "player_struggling": deaths > 0 or damage_taken >= 2,
            "player_thriving": enemies_beaten >= 2 and deaths == 0
        }
