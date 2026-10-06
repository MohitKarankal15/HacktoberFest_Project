"""
Core Game Engine for GEMMA WORLD: AI Adaptive Platformer
Manages the deterministic 60 FPS loop, physics, collisions, HUD, camera,
asynchronous Gemma 4 AI Brain, F3 telemetry debug panel, and rogue decision demo.
"""
import sys
import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    COLOR_WHITE, COLOR_BLACK, HUD_BG, HUD_BORDER, TEXT_GOLD, HEALTH_RED,
    AI_ACCENT, SKY_DAY_TOP, SKY_DAY_BOTTOM, SKY_NIGHT_TOP, SKY_NIGHT_BOTTOM,
    SKY_SUNSET_TOP, SKY_SUNSET_BOTTOM
)
from game.player import Player
from game.level import Level
from game.camera import Camera
from game.game_state import GameStateManager
from game.debug_panel import draw_debug_panel
from game.menu_manager import MenuManager
from game.sound_effects import SoundManager
from ai.gemma_brain import GemmaBrain
from ai.action_executor import execute_decision
from vision.gesture_detector import GestureDetector

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Engine state
        self.state = "menu"  # "menu", "playing", "paused", "howtoplay", "aibrain", "gameover", "victory"
        self.current_level_index = 1
        self.max_levels = 3

        # Fonts
        self.font_title = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_large = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16)

        # Core Game Systems
        self.level = Level(self.current_level_index)
        self.player = Player(self.level.spawn_x, self.level.spawn_y)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.state_manager = GameStateManager()
        self.state_manager.level = self.current_level_index
        self.menu_manager = MenuManager(
            self.font_title, self.font_large, self.font_medium, self.font_small
        )

        # AI & Vision Pipelines
        self.gemma_brain = GemmaBrain()
        self.gesture_detector = GestureDetector()
        self.sounds = SoundManager()

        # Notifications & Debug Panel
        self.notifications = []  # [{"text": str, "timer": float, "color": tuple}]
        self.show_debug_panel = False
        self.particles = []

    def show_notification(self, text, duration=3.5, color=AI_ACCENT):
        """Displays floating AI Director notification toast."""
        self.notifications.append({"text": text, "timer": duration, "color": color})

    def add_particles(self, x, y, count=8, color=(255, 230, 100)):
        """Spawns retro particle burst."""
        import random
        for _ in range(count):
            vx = (random.random() * 2 - 1) * 3.5
            vy = (random.random() * -3) - 1.0
            self.particles.append([x, y, vx, vy, color, 0.4])

    def handle_events(self):
        """Processes global keyboard inputs and UI state transitions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gemma_brain.is_running = False
                self.gesture_detector.stop()
                pygame.quit()
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                # F3 Debug Panel Toggle (always available)
                if event.key == pygame.K_F3:
                    self.show_debug_panel = not self.show_debug_panel

                # F4 Bad AI Decision Simulation Demo
                elif event.key == pygame.K_F4:
                    self.show_notification("⚡ SIMULATING ROGUE AI: 1000 ENEMIES REQUESTED!", 3.5, (255, 100, 100))
                    self.gemma_brain.trigger_bad_decision_demo()

                # F5 Force Immediate Gemma Query
                elif event.key == pygame.K_F5:
                    if self.state == "playing":
                        snapshot = self.state_manager.get_snapshot(self.player, self.level)
                        self.gemma_brain.request_decision(snapshot)
                        self.show_notification("AI: Forcing Gemma Brain observation...", 2.0, (200, 180, 255))

                # Menu state key handling
                if self.state == "menu":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.menu_manager.selected_index = (self.menu_manager.selected_index - 1) % 4
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.menu_manager.selected_index = (self.menu_manager.selected_index + 1) % 4
                    elif event.key == pygame.K_1:
                        self.state = "playing"
                    elif event.key == pygame.K_2:
                        self.state = "howtoplay"
                    elif event.key == pygame.K_3:
                        self.state = "aibrain"
                    elif event.key == pygame.K_4:
                        pygame.quit()
                        sys.exit(0)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        sel = self.menu_manager.selected_index
                        if sel == 0:
                            self.state = "playing"
                        elif sel == 1:
                            self.state = "howtoplay"
                        elif sel == 2:
                            self.state = "aibrain"
                        elif sel == 3:
                            pygame.quit()
                            sys.exit(0)

                elif self.state in ("howtoplay", "aibrain"):
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                        self.state = "menu"

                elif self.state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "paused"
                    elif event.key == pygame.K_SPACE:
                        if self.player.jump():
                            self.sounds.play("jump")
                    elif event.key == pygame.K_c:
                        # Toggle webcam gesture detector
                        if not self.gesture_detector.is_running:
                            ok = self.gesture_detector.start()
                            msg = "VISION ACTIVE: Webcam gestures listening!" if ok else "VISION: No webcam detected."
                            self.show_notification(msg, 3.0, (100, 255, 200))
                        else:
                            self.gesture_detector.stop()
                            self.show_notification("VISION: Webcam deactivated.", 2.5)

                elif self.state == "paused":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "playing"
                    elif event.key == pygame.K_m:
                        self.state = "menu"

                elif self.state in ("gameover", "victory"):
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "menu"

            elif event.type == pygame.KEYUP:
                if self.state == "playing" and event.key == pygame.K_SPACE:
                    self.player.cut_jump()

    def update_physics(self, dt):
        """Resolves horizontal and vertical movement and platform collisions."""
        player = self.player
        platforms = self.level.platforms

        # 1. Horizontal movement
        player.x += player.vx
        player_rect = player.rect

        for p in platforms:
            if not p.is_oneway and player_rect.colliderect(p.rect):
                if player.vx > 0:
                    player.x = p.rect.left - player.width
                    player.vx = 0
                elif player.vx < 0:
                    player.x = p.rect.right
                    player.vx = 0
                player_rect = player.rect

        # 2. Vertical movement & Gravity
        player.apply_gravity()
        old_bottom = player.y + player.height
        player.y += player.vy
        player_rect = player.rect

        player.is_grounded = False
        for p in platforms:
            if player_rect.colliderect(p.rect):
                if player.vy > 0:  # Falling downward
                    if p.is_oneway:
                        if old_bottom - player.vy <= p.rect.top + 8:
                            player.y = p.rect.top - player.height
                            player.vy = 0
                            player.is_grounded = True
                            player_rect = player.rect
                    else:
                        player.y = p.rect.top - player.height
                        player.vy = 0
                        player.is_grounded = True
                        player_rect = player.rect
                elif player.vy < 0 and not p.is_oneway:
                    player.y = p.rect.bottom
                    player.vy = 0
                    player_rect = player.rect

        # Pit fall check (bottom of world)
        if player.y > self.level.world_height + 100:
            self.state_manager.total_deaths += 1
            self.state_manager.record_event("player fell into pit")
            self.camera.add_shake(15.0)
            player.die()
            if player.lives <= 0:
                self.state = "gameover"

    def handle_combat_and_interactions(self, dt):
        """Resolves combat collisions with enemies and item collection."""
        player = self.player
        player_rect = player.rect

        # 1. Enemy interactions
        for enemy in self.level.enemies:
            if not enemy.is_alive:
                continue

            if player_rect.colliderect(enemy.rect):
                if player.vy > 1.0 and player.y + player.height <= enemy.y + (enemy.height * 0.55):
                    defeated = enemy.take_stomp()
                    player.vy = -10.5
                    self.sounds.play("stomp")
                    self.add_particles(enemy.x + enemy.width / 2, enemy.y, 12, (255, 100, 200))
                    self.camera.add_shake(6.0)
                    
                    if defeated:
                        self.state_manager.enemies_defeated += 1
                        player.score += 200
                        self.state_manager.record_event(f"player defeated {enemy.enemy_type} enemy")
                else:
                    result = player.take_damage(enemy.damage)
                    self.sounds.play("hurt")
                    if result == "shield_absorbed":
                        self.state_manager.record_event("player lost shield to enemy attack")
                        self.camera.add_shake(8.0)
                    elif result == "hurt":
                        self.state_manager.record_event(f"player lost health from {enemy.enemy_type} enemy")
                        self.camera.add_shake(12.0)
                    elif result == "died":
                        self.state_manager.total_deaths += 1
                        self.state_manager.record_event(f"player died from {enemy.enemy_type} enemy")
                        self.camera.add_shake(18.0)
                        if player.lives <= 0:
                            self.state = "gameover"

        # 2. Coin collections
        for coin in self.level.coins:
            if not coin.is_collected and player_rect.colliderect(coin.rect):
                coin.is_collected = True
                player.add_coins(coin.value)
                self.sounds.play("coin")
                self.state_manager.coins_collected += 1
                self.add_particles(coin.x + coin.size / 2, coin.y, 6, (255, 230, 80))
                self.state_manager.record_event("player collected coin")

        # 3. Power-up collections
        for pu in self.level.powerups:
            if not pu.is_collected and player_rect.colliderect(pu.rect):
                pu.is_collected = True
                player.activate_powerup(pu.powerup_type)
                self.sounds.play("powerup")
                self.state_manager.powerups_used += 1
                self.add_particles(pu.x + pu.size / 2, pu.y, 16, (100, 240, 255))
                self.show_notification(f"POWER-UP: {pu.powerup_type.replace('_', ' ').upper()}!", 3.0)
                self.state_manager.record_event(f"player collected {pu.powerup_type.replace('_', ' ')}")

    def advance_level(self):
        """Loads next level or transitions to victory."""
        if self.current_level_index < self.max_levels:
            self.current_level_index += 1
            self.state_manager.level = self.current_level_index
            self.level.load_level(self.current_level_index)
            self.player.x = float(self.level.spawn_x)
            self.player.y = float(self.level.spawn_y)
            self.player.spawn_x = self.level.spawn_x
            self.player.spawn_y = self.level.spawn_y
            self.state_manager.record_event(f"player entered level {self.current_level_index}")
            self.show_notification(f"STAGE CLEARED! WELCOME TO LEVEL {self.current_level_index}", 4.0, TEXT_GOLD)
        else:
            self.state = "victory"

    def update(self, dt):
        """Main update tick."""
        if self.state != "playing":
            return

        # Player continuous input
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(dt)

        self.update_physics(dt)
        self.handle_combat_and_interactions(dt)

        # Update level entities
        event = self.level.update(dt, self.player)
        if event == "level_complete":
            self.advance_level()
        elif event == "checkpoint_reached":
            self.show_notification("CHECKPOINT ACTIVATED!", 2.5, (100, 255, 150))
            self.state_manager.record_event("player completed checkpoint")

        # Check visual gesture events from webcam if active
        vis_event = self.gesture_detector.get_latest_event()
        if vis_event:
            ve = vis_event.get("visual_event")
            self.state_manager.record_event(f"visual gesture recognized: {ve}")
            if ve == "open_hand":
                self.state = "paused"
                self.show_notification("GESTURE: OPEN HAND → WORLD PAUSED!", 3.0)
            elif ve == "thumbs_up":
                self.show_notification("GESTURE: THUMBS UP → POWER-UP REQUESTED!", 3.0)
                self.gemma_brain.request_decision(self.state_manager.get_snapshot(self.player, self.level))
            elif ve == "fist":
                self.show_notification("GESTURE: FIST → CHALLENGE REQUESTED!", 3.0)
                self.gemma_brain.request_decision(self.state_manager.get_snapshot(self.player, self.level))

        # Check for completed AI decisions from background worker
        snapshot = self.state_manager.get_snapshot(self.player, self.level)
        val_result = self.gemma_brain.update(dt, snapshot)
        if val_result:
            self.sounds.play("ai_pulse")
            if val_result.status == "REJECTED":
                self.show_notification(f"🛡️ AI REJECTED: {val_result.reason}", 4.5, HEALTH_RED)
            execute_decision(val_result, self)

        # Update particles
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.2
            p[5] -= dt
        self.particles = [p for p in self.particles if p[5] > 0]

        # Update notifications
        for notif in self.notifications:
            notif["timer"] -= dt
        self.notifications = [n for n in self.notifications if n["timer"] > 0]

    def render_sky(self):
        """Renders sky gradient according to world weather/time."""
        top_color, bottom_color = SKY_DAY_TOP, SKY_DAY_BOTTOM
        if self.state_manager.time_of_day == "sunset":
            top_color, bottom_color = SKY_SUNSET_TOP, SKY_SUNSET_BOTTOM
        elif self.state_manager.time_of_day == "night":
            top_color, bottom_color = SKY_NIGHT_TOP, SKY_NIGHT_BOTTOM

        height = SCREEN_HEIGHT
        width = SCREEN_WIDTH
        for y in range(0, height, 4):
            ratio = y / height
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.rect(self.screen, (r, g, b), (0, y, width, 4))

    def render_hud(self):
        """Renders HUD: Hearts, Level, Coins, Score, Difficulty, Buffs."""
        # Top-Left: Health & Lives
        hud_card = pygame.Surface((310, 80), pygame.SRCALPHA)
        pygame.draw.rect(hud_card, HUD_BG, (0, 0, 310, 80), border_radius=10)
        pygame.draw.rect(hud_card, HUD_BORDER, (0, 0, 310, 80), width=2, border_radius=10)
        self.screen.blit(hud_card, (20, 20))

        # Hearts
        lives_str = "❤️ " * self.player.lives
        lives_text = self.font_medium.render(lives_str, True, HEALTH_RED)
        self.screen.blit(lives_text, (35, 30))

        # Health bar
        bar_w, bar_h = 160, 14
        bar_x, bar_y = 35, 60
        pygame.draw.rect(self.screen, (60, 60, 70), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        fill_w = int((self.player.health / self.player.max_health) * bar_w)
        if fill_w > 0:
            pygame.draw.rect(self.screen, HEALTH_RED, (bar_x, bar_y, fill_w, bar_h), border_radius=3)
        hp_text = self.font_small.render(f"{int(self.player.health)} HP", True, COLOR_WHITE)
        self.screen.blit(hp_text, (bar_x + bar_w + 12, bar_y - 2))

        # Top-Center: Current Level
        center_card = pygame.Surface((220, 48), pygame.SRCALPHA)
        pygame.draw.rect(center_card, HUD_BG, (0, 0, 220, 48), border_radius=8)
        pygame.draw.rect(center_card, HUD_BORDER, (0, 0, 220, 48), width=2, border_radius=8)
        cx = (SCREEN_WIDTH - 220) // 2
        self.screen.blit(center_card, (cx, 20))
        lvl_text = self.font_medium.render(f"LEVEL {self.current_level_index}", True, COLOR_WHITE)
        self.screen.blit(lvl_text, (cx + (220 - lvl_text.get_width()) // 2, 32))

        # Top-Right: Coins & Score
        right_card = pygame.Surface((260, 80), pygame.SRCALPHA)
        pygame.draw.rect(right_card, HUD_BG, (0, 0, 260, 80), border_radius=10)
        pygame.draw.rect(right_card, HUD_BORDER, (0, 0, 260, 80), width=2, border_radius=10)
        rx = SCREEN_WIDTH - 280
        self.screen.blit(right_card, (rx, 20))

        coin_text = self.font_medium.render(f"🪙 COINS: {self.player.coins}", True, TEXT_GOLD)
        score_text = self.font_small.render(f"SCORE: {self.player.score:05d}", True, COLOR_WHITE)
        self.screen.blit(coin_text, (rx + 20, 30))
        self.screen.blit(score_text, (rx + 20, 60))

        # Bottom-Left: AI Difficulty Meter
        ai_card = pygame.Surface((240, 46), pygame.SRCALPHA)
        pygame.draw.rect(ai_card, HUD_BG, (0, 0, 240, 46), border_radius=8)
        pygame.draw.rect(ai_card, HUD_BORDER, (0, 0, 240, 46), width=2, border_radius=8)
        self.screen.blit(ai_card, (20, SCREEN_HEIGHT - 66))
        diff_text = self.font_small.render(
            f"AI DIFFICULTY: {self.state_manager.difficulty}/10", True, (210, 170, 255)
        )
        self.screen.blit(diff_text, (35, SCREEN_HEIGHT - 52))

        # Render floating AI notifications
        notif_y = 120
        for notif in self.notifications:
            txt = notif["text"]
            surf = self.font_medium.render(f"⚡ {txt}", True, notif["color"])
            bg = pygame.Surface((surf.get_width() + 30, 40), pygame.SRCALPHA)
            pygame.draw.rect(bg, (20, 15, 35, 230), (0, 0, bg.get_width(), 40), border_radius=8)
            pygame.draw.rect(bg, notif["color"], (0, 0, bg.get_width(), 40), width=2, border_radius=8)
            nx = (SCREEN_WIDTH - bg.get_width()) // 2
            self.screen.blit(bg, (nx, notif_y))
            self.screen.blit(surf, (nx + 15, notif_y + 8))
            notif_y += 50

    def draw(self):
        """Renders world and active state."""
        self.render_sky()

        # If in menu states, render respective UI
        if self.state == "menu":
            self.menu_manager.render_title_menu(self.screen)
        elif self.state == "howtoplay":
            self.menu_manager.render_how_to_play(self.screen)
        elif self.state == "aibrain":
            self.menu_manager.render_ai_brain_explainer(self.screen)
        elif self.state in ("playing", "paused", "gameover", "victory"):
            cam_x, cam_y = self.camera.update(
                self.player.rect, self.level.world_width, self.level.world_height
            )

            # Draw Level and Entities
            self.level.draw(self.screen, cam_x, cam_y)
            self.player.draw(self.screen, cam_x, cam_y)

            # Draw particles
            for p in self.particles:
                px = int(p[0] - cam_x)
                py = int(p[1] - cam_y)
                pygame.draw.circle(self.screen, p[4], (px, py), 3)

            # Draw HUD
            self.render_hud()

            # Render Pause Overlay
            if self.state == "paused":
                ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                ov.fill((10, 12, 20, 180))
                self.screen.blit(ov, (0, 0))
                p_txt = self.font_title.render("GAME PAUSED", True, TEXT_GOLD)
                s_txt = self.font_medium.render("Press ESC to Resume | M for Main Menu", True, COLOR_WHITE)
                self.screen.blit(p_txt, ((SCREEN_WIDTH - p_txt.get_width()) // 2, 280))
                self.screen.blit(s_txt, ((SCREEN_WIDTH - s_txt.get_width()) // 2, 350))

            elif self.state == "gameover":
                self.render_game_over_screen()
            elif self.state == "victory":
                self.render_victory_screen()

        # Draw F3 Debug Panel if toggled
        if self.show_debug_panel:
            draw_debug_panel(
                self.screen, self.gemma_brain, self.state_manager,
                self.font_medium, self.font_small
            )

        pygame.display.flip()

    def render_game_over_screen(self):
        """Displays Game Over screen with AI statistics."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 12, 18, 220))
        self.screen.blit(overlay, (0, 0))

        card_w, card_h = 560, 370
        cx = (SCREEN_WIDTH - card_w) // 2
        cy = (SCREEN_HEIGHT - card_h) // 2
        pygame.draw.rect(self.screen, HUD_BG, (cx, cy, card_w, card_h), border_radius=14)
        pygame.draw.rect(self.screen, HEALTH_RED, (cx, cy, card_w, card_h), width=2, border_radius=14)

        t_surf = self.font_title.render("GAME OVER", True, HEALTH_RED)
        s_surf = self.font_medium.render(f"Final Score: {self.player.score}", True, COLOR_WHITE)
        c_surf = self.font_medium.render(f"Coins Collected: {self.player.coins}", True, TEXT_GOLD)
        ai_surf1 = self.font_small.render(f"Total AI Decisions: {self.state_manager.ai_decisions_count}", True, (200, 180, 255))
        ai_surf2 = self.font_small.render(f"Successful Actions: {self.state_manager.ai_accepted_count}", True, (150, 255, 180))
        ai_surf3 = self.font_small.render(f"Rejected Actions: {self.state_manager.ai_rejected_count}", True, (255, 150, 150))
        r_surf = self.font_medium.render("Press 'R' to Restart | ESC for Menu", True, (180, 220, 255))

        self.screen.blit(t_surf, (cx + (card_w - t_surf.get_width()) // 2, cy + 25))
        self.screen.blit(s_surf, (cx + 50, cy + 95))
        self.screen.blit(c_surf, (cx + 50, cy + 130))
        self.screen.blit(ai_surf1, (cx + 50, cy + 175))
        self.screen.blit(ai_surf2, (cx + 50, cy + 205))
        self.screen.blit(ai_surf3, (cx + 50, cy + 235))
        self.screen.blit(r_surf, (cx + (card_w - r_surf.get_width()) // 2, cy + 300))

    def render_victory_screen(self):
        """Displays Victory screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 12, 18, 220))
        self.screen.blit(overlay, (0, 0))

        card_w, card_h = 560, 320
        cx = (SCREEN_WIDTH - card_w) // 2
        cy = (SCREEN_HEIGHT - card_h) // 2
        pygame.draw.rect(self.screen, HUD_BG, (cx, cy, card_w, card_h), border_radius=14)
        pygame.draw.rect(self.screen, TEXT_GOLD, (cx, cy, card_w, card_h), width=2, border_radius=14)

        t_surf = self.font_title.render("VICTORY! MISSION COMPLETE", True, TEXT_GOLD)
        s_surf = self.font_medium.render(f"Final Score: {self.player.score}", True, COLOR_WHITE)
        c_surf = self.font_medium.render(f"Coins: {self.player.coins}", True, TEXT_GOLD)
        r_surf = self.font_medium.render("Press 'R' to Play Again | ESC for Menu", True, (180, 220, 255))

        self.screen.blit(t_surf, (cx + (card_w - t_surf.get_width()) // 2, cy + 40))
        self.screen.blit(s_surf, (cx + (card_w - s_surf.get_width()) // 2, cy + 120))
        self.screen.blit(c_surf, (cx + (card_w - c_surf.get_width()) // 2, cy + 160))
        self.screen.blit(r_surf, (cx + (card_w - r_surf.get_width()) // 2, cy + 240))

    def restart_game(self):
        """Resets the entire game to Level 1."""
        self.current_level_index = 1
        self.state_manager = GameStateManager()
        self.state_manager.level = 1
        self.level.load_level(1)
        self.player = Player(self.level.spawn_x, self.level.spawn_y)
        self.state = "playing"

    def run(self):
        """Main game loop."""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
