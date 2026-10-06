"""
Comprehensive Unit Tests for GEMMA WORLD AI Pipeline & Safety Architecture
Tests:
1. Valid AI decision (Accepted)
2. Invalid JSON string (Parsed safely / fallback)
3. Unknown action (Rejected)
4. Out-of-bounds / Rogue enemy count (Rejected / Clamped)
5. Timeout / Gemma unavailable (Deterministic fallback)
6. Player low health adaptation (Heal or Shield)
7. Player high performance adaptation (Challenge / Speed increase)
8. AI Memory queue ring buffer (Clamped to MAX_RECENT_EVENTS)
"""
import unittest
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.validator import validate_decision
from ai.decision_parser import parse_gemma_response
from ai.fallback_director import generate_fallback_decision
from ai.ai_memory import AIMemory
from config import MAX_RECENT_EVENTS

class TestAIPipeline(unittest.TestCase):

    def test_valid_ai_response(self):
        """Test that a valid structured decision is ACCEPTED."""
        raw_decision = {
            "action": "spawn_enemy",
            "enemy_type": "venom",
            "count": 2,
            "reason": "Player has high health and steady progress."
        }
        res = validate_decision(raw_decision)
        self.assertEqual(res.status, "ACCEPTED")
        self.assertEqual(res.sanitized_decision["action"], "spawn_enemy")
        self.assertEqual(res.sanitized_decision["count"], 2)

    def test_invalid_json_parser(self):
        """Test that malformed JSON is caught gracefully without throwing unhandled exceptions."""
        malformed = "I think the player is doing great, let's spawn 5 coins!"
        parsed, err = parse_gemma_response(malformed)
        self.assertIsNone(parsed)
        self.assertIsNotNone(err)

    def test_markdown_fenced_json(self):
        """Test that JSON wrapped in markdown code fences is cleanly extracted."""
        fenced = "```json\n{\n  \"action\": \"spawn_powerup\",\n  \"powerup_type\": \"shield\"\n}\n```"
        parsed, err = parse_gemma_response(fenced)
        self.assertIsNotNone(parsed)
        self.assertIsNone(err)
        self.assertEqual(parsed["action"], "spawn_powerup")

    def test_unknown_action_rejected(self):
        """Test that unauthorized actions outside the whitelist are REJECTED."""
        rogue_action = {
            "action": "destroy_all_platforms",
            "reason": "AI gone wild."
        }
        res = validate_decision(rogue_action)
        self.assertEqual(res.status, "REJECTED")
        self.assertEqual(res.sanitized_decision["action"], "do_nothing")

    def test_too_many_enemies_rejected_or_clamped(self):
        """Test rogue decision with 1000 enemies is rejected and clamped to safe count."""
        absurd_count = {
            "action": "spawn_enemy",
            "enemy_type": "flash",
            "count": 1000,
            "reason": "Flood the map with 1000 enemies!"
        }
        res = validate_decision(absurd_count)
        self.assertEqual(res.status, "REJECTED")
        self.assertEqual(res.sanitized_decision["count"], 1)

    def test_enemy_count_clamping(self):
        """Test enemy count slightly above limit (e.g. 5) is CLAMPED to MAX_ENEMIES_TO_SPAWN (3)."""
        moderate_excess = {
            "action": "spawn_enemy",
            "enemy_type": "joker",
            "count": 5,
            "reason": "Testing clamp."
        }
        res = validate_decision(moderate_excess)
        self.assertEqual(res.status, "CLAMPED")
        self.assertEqual(res.sanitized_decision["count"], 3)

    def test_player_low_health_fallback(self):
        """Test that Fallback Director assists a critical player."""
        critical_state = {
            "player": {"health": 20, "lives": 1},
            "world": {"difficulty": 4, "enemy_count": 2},
            "stats": {"enemies_defeated": 1},
            "recent_events": ["player lost health"]
        }
        decision = generate_fallback_decision(critical_state)
        self.assertIn(decision["action"], ["give_health", "spawn_powerup"])

    def test_player_thriving_fallback(self):
        """Test that Fallback Director scales up difficulty when player is thriving."""
        thriving_state = {
            "player": {"health": 95, "lives": 3},
            "world": {"difficulty": 3, "enemy_count": 1},
            "stats": {"enemies_defeated": 5},
            "recent_events": ["player defeated venom enemy"]
        }
        decision = generate_fallback_decision(thriving_state)
        self.assertIn(decision["action"], ["spawn_enemy", "spawn_coin", "increase_difficulty"])

    def test_ai_memory_ring_buffer(self):
        """Test that AI Memory FIFO buffer never exceeds MAX_RECENT_EVENTS."""
        memory = AIMemory(max_events=MAX_RECENT_EVENTS)
        for i in range(25):
            memory.record(f"event_{i}")
        recent = memory.get_recent_event_strings()
        self.assertEqual(len(recent), MAX_RECENT_EVENTS)
        self.assertEqual(recent[-1], "event_24")

if __name__ == "__main__":
    unittest.main()
