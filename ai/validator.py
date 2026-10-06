"""
AI Safety Validator for GEMMA WORLD
Enforces strict boundaries, whitelists, parameter clamping, and rogue decision filtering.
"""
from config import (
    ALLOWED_ACTIONS, MAX_ENEMIES_TO_SPAWN, MAX_SPEED_MULTIPLIER,
    MIN_SPEED_MULTIPLIER, MAX_POWERUPS_TO_SPAWN, MAX_PLATFORM_CHANGES,
    MAX_HEALTH_GIVE, MIN_DIFFICULTY, MAX_DIFFICULTY
)

class ValidationResult:
    def __init__(self, status, sanitized_decision, reason, original_decision=None):
        self.status = status  # "ACCEPTED", "CLAMPED", "REJECTED"
        self.sanitized_decision = sanitized_decision
        self.reason = reason
        self.original_decision = original_decision or sanitized_decision

    @property
    def is_executable(self):
        return self.status in ("ACCEPTED", "CLAMPED")

    def __repr__(self):
        return f"<ValidationResult status={self.status} action={self.sanitized_decision.get('action')} reason='{self.reason}'>"

def validate_decision(raw_decision, current_state=None):
    """
    Validates and sanitizes a decision dictionary from the AI.
    Returns ValidationResult with status "ACCEPTED", "CLAMPED", or "REJECTED".
    """
    if not isinstance(raw_decision, dict):
        return ValidationResult(
            status="REJECTED",
            sanitized_decision={"action": "do_nothing", "reason": "Non-dictionary input received."},
            reason="Payload is not a valid dictionary.",
            original_decision=raw_decision
        )

    action = raw_decision.get("action")
    ai_reason = raw_decision.get("reason", "No reason provided.")

    # 1. Whitelist Action Check
    if action not in ALLOWED_ACTIONS:
        return ValidationResult(
            status="REJECTED",
            sanitized_decision={"action": "do_nothing", "reason": f"Unknown action: '{action}'"},
            reason=f"Action '{action}' is not in allowed actions whitelist.",
            original_decision=raw_decision
        )

    # 2. Parameter bounds checking & clamping per action
    sanitized = dict(raw_decision)
    sanitized["action"] = action
    sanitized["reason"] = ai_reason

    if action == "do_nothing":
        return ValidationResult("ACCEPTED", sanitized, "Safe idle action approved.")

    elif action == "spawn_enemy":
        enemy_type = str(raw_decision.get("enemy_type", "walker")).lower()
        if enemy_type not in ["walker", "chaser", "fast"]:
            enemy_type = "walker"
        sanitized["enemy_type"] = enemy_type

        count = raw_decision.get("count", 1)
        try:
            count = int(count)
        except (ValueError, TypeError):
            count = 1

        # Demonstration of Rogue / Bad Decision detection
        if count > 10:
            # Massive rogue number (e.g. 1000) -> Outright REJECT and clamp to safe fallback = 1
            sanitized["count"] = 1
            return ValidationResult(
                status="REJECTED",
                sanitized_decision=sanitized,
                reason=f"Enemy count ({count}) exceeds maximum safety threshold (10). Clamped to 1 as safe fallback.",
                original_decision=raw_decision
            )
        elif count > MAX_ENEMIES_TO_SPAWN:
            # Minor excess -> CLAMP
            sanitized["count"] = MAX_ENEMIES_TO_SPAWN
            return ValidationResult(
                status="CLAMPED",
                sanitized_decision=sanitized,
                reason=f"Enemy count clamped from {count} to safe limit {MAX_ENEMIES_TO_SPAWN}.",
                original_decision=raw_decision
            )
        elif count < 1:
            sanitized["count"] = 1

        return ValidationResult("ACCEPTED", sanitized, "Enemy spawn parameters verified.")

    elif action == "spawn_coin":
        count = raw_decision.get("count", 2)
        try:
            count = int(count)
        except (ValueError, TypeError):
            count = 2

        if count > 5:
            sanitized["count"] = 5
            return ValidationResult("CLAMPED", sanitized, f"Coin count clamped from {count} to 5.")
        elif count < 1:
            sanitized["count"] = 1
        return ValidationResult("ACCEPTED", sanitized, "Coin spawn approved.")

    elif action == "spawn_powerup":
        pu_type = str(raw_decision.get("powerup_type", "health_crystal")).lower()
        if pu_type not in ["health_crystal", "speed_boost", "shield", "magnet"]:
            pu_type = "health_crystal"
        sanitized["powerup_type"] = pu_type
        return ValidationResult("ACCEPTED", sanitized, f"Power-up {pu_type} approved.")

    elif action == "change_enemy_speed":
        multiplier = raw_decision.get("multiplier", 1.0)
        try:
            multiplier = float(multiplier)
        except (ValueError, TypeError):
            multiplier = 1.0

        if multiplier > MAX_SPEED_MULTIPLIER:
            sanitized["multiplier"] = MAX_SPEED_MULTIPLIER
            return ValidationResult("CLAMPED", sanitized, f"Speed multiplier clamped to max {MAX_SPEED_MULTIPLIER}x.")
        elif multiplier < MIN_SPEED_MULTIPLIER:
            sanitized["multiplier"] = MIN_SPEED_MULTIPLIER
            return ValidationResult("CLAMPED", sanitized, f"Speed multiplier clamped to min {MIN_SPEED_MULTIPLIER}x.")

        sanitized["multiplier"] = multiplier
        return ValidationResult("ACCEPTED", sanitized, "Enemy speed adjustment approved.")

    elif action == "give_health":
        amount = raw_decision.get("amount", 20)
        try:
            amount = int(amount)
        except (ValueError, TypeError):
            amount = 20

        if amount > MAX_HEALTH_GIVE:
            sanitized["amount"] = MAX_HEALTH_GIVE
            return ValidationResult("CLAMPED", sanitized, f"Health gift clamped to maximum {MAX_HEALTH_GIVE} HP.")
        elif amount < 5:
            sanitized["amount"] = 5
        sanitized["amount"] = amount
        return ValidationResult("ACCEPTED", sanitized, f"Health bonus {sanitized['amount']} HP approved.")

    elif action in ("increase_difficulty", "decrease_difficulty"):
        step = raw_decision.get("step", 1)
        try:
            step = int(step)
        except (ValueError, TypeError):
            step = 1
        sanitized["step"] = min(2, max(1, step))
        return ValidationResult("ACCEPTED", sanitized, f"Difficulty step {sanitized['step']} approved.")

    elif action == "change_weather":
        weather = str(raw_decision.get("weather", "clear")).lower()
        if weather not in ["clear", "rain", "windy", "sunset", "night"]:
            weather = "clear"
        sanitized["weather"] = weather
        return ValidationResult("ACCEPTED", sanitized, f"Weather transition to '{weather}' approved.")

    elif action in ("create_platform", "remove_platform"):
        ptype = str(raw_decision.get("platform_type", "floating")).lower()
        if ptype not in ["floating", "oneway"]:
            ptype = "floating"
        sanitized["platform_type"] = ptype
        return ValidationResult("ACCEPTED", sanitized, f"Platform modification approved.")

    elif action == "activate_event":
        ename = str(raw_decision.get("event_name", "coin_rush")).lower()
        if ename not in ["coin_rush", "gravity_anomaly", "enemy_swarm"]:
            ename = "coin_rush"
        sanitized["event_name"] = ename
        return ValidationResult("ACCEPTED", sanitized, f"World event '{ename}' approved.")

    return ValidationResult("ACCEPTED", sanitized, "Decision approved.")
