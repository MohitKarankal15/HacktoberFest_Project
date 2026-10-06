"""
Centralized Game State Manager for GEMMA WORLD
Produces the exact structured state dictionary observed by the Gemma AI Director.
"""
import json
from config import MAX_RECENT_EVENTS

class GameStateManager:
    def __init__(self):
        self.level = 1
        self.difficulty = 3  # 1 to 10
        self.weather = "clear"  # clear, rain, windy, storm
        self.time_of_day = "day"  # day, sunset, night
        
        # Historical metrics
        self.total_deaths = 0
        self.enemies_defeated = 0
        self.coins_collected = 0
        self.powerups_used = 0

        # AI tracking metrics
        self.ai_decisions_count = 0
        self.ai_accepted_count = 0
        self.ai_rejected_count = 0
        
        # Rolling recent events buffer (max 10)
        self.recent_events = []

    def record_event(self, event_str):
        """Appends an event to the rolling recent events buffer."""
        self.recent_events.append(event_str)
        if len(self.recent_events) > MAX_RECENT_EVENTS:
            self.recent_events.pop(0)

    def get_snapshot(self, player, level):
        """
        Builds the canonical JSON-serializable snapshot of the game
        ready for observation by Gemma 4.
        """
        active_enemies = len([e for e in level.enemies if e.is_alive])
        active_platforms = len(level.platforms)

        state = {
            "level": self.level,
            "player": {
                "health": int(player.health),
                "max_health": int(player.max_health),
                "lives": int(player.lives),
                "coins": int(player.coins),
                "score": int(player.score),
                "x": int(player.x),
                "y": int(player.y),
                "shield_active": bool(player.has_shield),
                "speed_boost_active": bool(player.speed_boost_timer > 0),
                "magnet_active": bool(player.magnet_timer > 0)
            },
            "world": {
                "enemy_count": active_enemies,
                "platform_count": active_platforms,
                "weather": self.weather,
                "time": self.time_of_day,
                "difficulty": self.difficulty
            },
            "stats": {
                "total_deaths": self.total_deaths,
                "enemies_defeated": self.enemies_defeated,
                "coins_collected": self.coins_collected
            },
            "recent_events": list(self.recent_events)
        }
        return state

    def to_json(self, player, level, indent=2):
        """Returns pretty JSON string of snapshot."""
        return json.dumps(self.get_snapshot(player, level), indent=indent)
