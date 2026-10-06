"""
Rule-Based Fallback Game Director for GEMMA WORLD
Executes deterministic heuristic decisions when Gemma 4 is offline, times out (>3.0s),
or returns malformed output.
"""
def generate_fallback_decision(game_state):
    """
    Evaluates current game state and produces a balanced, safe decision.
    """
    player = game_state.get("player", {})
    world = game_state.get("world", {})
    stats = game_state.get("stats", {})
    recent_events = game_state.get("recent_events", [])

    health = player.get("health", 100)
    lives = player.get("lives", 3)
    difficulty = world.get("difficulty", 3)
    enemy_count = world.get("enemy_count", 0)

    # Rule 1: Emergency health assistance if player is low on health and lives
    if health <= 35 and lives <= 2:
        return {
            "action": "give_health",
            "amount": 25,
            "reason": "Fallback Director: Player health is critical (emergency aid)."
        }

    # Rule 2: Provide shield or health crystal if player is moderately damaged
    if health <= 45:
        return {
            "action": "spawn_powerup",
            "powerup_type": "shield" if not player.get("shield_active") else "health_crystal",
            "reason": "Fallback Director: Assisting player under high pressure."
        }

    # Rule 3: Recovery assistance after recent deaths or pit falls
    if any("died" in str(e) or "pit" in str(e) for e in recent_events[-3:]):
        return {
            "action": "spawn_powerup",
            "powerup_type": "speed_boost",
            "reason": "Fallback Director: Assisting player mobility after recent setback."
        }

    # Rule 4: Scale up challenge if player has high health and low enemy presence
    if health >= 80 and enemy_count <= 2:
        if difficulty < 6:
            return {
                "action": "spawn_enemy",
                "enemy_type": "fast" if difficulty >= 4 else "walker",
                "count": 1,
                "reason": "Fallback Director: Player performing well; adding light challenge."
            }

    # Rule 5: Reward with coins if doing well
    if health >= 90 and difficulty >= 4:
        return {
            "action": "spawn_coin",
            "count": 3,
            "reason": "Fallback Director: Rewarding high-performance player with coins."
        }

    # Default idle
    return {
        "action": "do_nothing",
        "reason": "Fallback Director: World conditions are stable."
    }
