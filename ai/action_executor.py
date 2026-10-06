"""
Action Executor for GEMMA WORLD
Executes safely validated AI decisions onto the active game engine and level.
"""
from game.enemy import Enemy
from game.coin import Coin
from game.powerup import PowerUp
from game.platform import Platform

def execute_decision(validation_result, game_engine):
    """
    Executes a sanitized decision from the AI validator.
    Returns: action summary string
    """
    decision = validation_result.sanitized_decision
    action = decision.get("action", "do_nothing")
    reason = decision.get("reason", "")
    player = game_engine.player
    level = game_engine.level
    state_mgr = game_engine.state_manager

    # Update stats
    state_mgr.ai_decisions_count += 1
    if validation_result.status in ("ACCEPTED", "CLAMPED"):
        state_mgr.ai_accepted_count += 1
    else:
        state_mgr.ai_rejected_count += 1

    summary = f"Action: {action}"

    if action == "do_nothing":
        return "Gemma: World stable, observing player."

    elif action == "spawn_enemy":
        enemy_type = decision.get("enemy_type", "web_hero")
        count = decision.get("count", 1)
        # Spawn safely ahead of player
        spawn_base_x = player.x + 380
        for i in range(count):
            ex = min(level.world_width - 200, spawn_base_x + (i * 90))
            ey = player.y - 20
            # Find nearest platform below
            for p in level.platforms:
                if p.rect.left <= ex <= p.rect.right and p.rect.top >= ey:
                    ey = p.rect.top - 40
                    break
            level.enemies.append(Enemy(ex, ey, enemy_type))
        game_engine.show_notification(f"GEMMA: Spawned {count}x {enemy_type.upper()}!", 3.5, (255, 100, 100))
        summary = f"Spawned {count} {enemy_type} enemy(ies)"

    elif action == "spawn_coin":
        count = decision.get("count", 3)
        spawn_base_x = player.x + 220
        for i in range(count):
            cx = min(level.world_width - 150, spawn_base_x + (i * 45))
            cy = max(100, player.y - 40 - (i % 2) * 20)
            level.coins.append(Coin(cx, cy))
        game_engine.show_notification(f"GEMMA: Spawned {count} coins for you!", 3.0, (255, 215, 0))
        summary = f"Spawned {count} coins"

    elif action == "spawn_powerup":
        pu_type = decision.get("powerup_type", "health_crystal")
        px = min(level.world_width - 200, player.x + 240)
        py = max(100, player.y - 40)
        level.powerups.append(PowerUp(px, py, pu_type))
        clean_name = pu_type.replace('_', ' ').upper()
        game_engine.show_notification(f"GEMMA: Dropped {clean_name}!", 3.5, (100, 230, 255))
        summary = f"Spawned power-up {pu_type}"

    elif action == "change_enemy_speed":
        multiplier = decision.get("multiplier", 1.0)
        for enemy in level.enemies:
            enemy.speed_multiplier = multiplier
        game_engine.show_notification(f"GEMMA: Enemy speed adjusted ({multiplier:.1f}x)!", 3.0)
        summary = f"Enemy speed set to {multiplier:.1f}x"

    elif action == "create_platform":
        ptype = decision.get("platform_type", "floating")
        px = player.x + 180
        py = max(150, player.y + 40)
        new_plat = Platform(px, py, 180, 24, ptype, is_dynamic=True, lifetime=20.0)
        level.platforms.append(new_plat)
        game_engine.show_notification("GEMMA: Created helpful platform!", 3.0, (140, 90, 255))
        summary = f"Created dynamic {ptype} platform"

    elif action == "remove_platform":
        # Remove an oldest dynamic platform if available
        dyn_plats = [p for p in level.platforms if p.is_dynamic]
        if dyn_plats:
            level.platforms.remove(dyn_plats[0])
            game_engine.show_notification("GEMMA: Dissolved dynamic platform!", 3.0)
            summary = "Removed 1 dynamic platform"
        else:
            summary = "No dynamic platforms to remove"

    elif action == "change_weather":
        weather = decision.get("weather", "clear")
        state_mgr.weather = weather
        if weather in ("sunset", "night"):
            state_mgr.time_of_day = weather
        else:
            state_mgr.time_of_day = "day"
        game_engine.show_notification(f"GEMMA: Weather changed to {weather.upper()}!", 3.5)
        summary = f"Weather changed to {weather}"

    elif action == "increase_difficulty":
        step = decision.get("step", 1)
        state_mgr.difficulty = min(10, state_mgr.difficulty + step)
        game_engine.show_notification(f"GEMMA: Difficulty increased to {state_mgr.difficulty}/10!", 3.0, (255, 80, 80))
        summary = f"Difficulty increased to {state_mgr.difficulty}"

    elif action == "decrease_difficulty":
        step = decision.get("step", 1)
        state_mgr.difficulty = max(1, state_mgr.difficulty - step)
        game_engine.show_notification(f"GEMMA: Difficulty eased to {state_mgr.difficulty}/10!", 3.0, (100, 255, 150))
        summary = f"Difficulty decreased to {state_mgr.difficulty}"

    elif action == "give_health":
        amount = decision.get("amount", 20)
        player.heal(amount)
        game_engine.show_notification(f"GEMMA: Blessed Nova with +{amount} HP!", 3.0, (80, 255, 120))
        summary = f"Gave {amount} HP"

    elif action == "activate_event":
        ename = decision.get("event_name", "coin_rush")
        if ename == "coin_rush":
            for i in range(5):
                level.coins.append(Coin(player.x + 80 + i * 40, player.y - 50))
            game_engine.show_notification("⚡ WORLD EVENT: COIN RUSH! ⚡", 4.0, (255, 230, 80))
        elif ename == "enemy_swarm":
            level.enemies.append(Enemy(player.x + 350, player.y - 20, "web_hero"))
            level.enemies.append(Enemy(player.x + 440, player.y - 20, "dark_knight"))
            game_engine.show_notification("⚠️ WORLD EVENT: ENEMY SWARM! ⚠️", 4.0, (255, 80, 80))
        summary = f"World event '{ename}' triggered"

    return summary
