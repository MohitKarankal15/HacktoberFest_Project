"""
Menu and UI screens manager for GEMMA WORLD
Implements Title Menu, How-to-Play, and AI Brain Architecture explainer.
"""
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, HUD_BG, HUD_BORDER, TEXT_GOLD, AI_ACCENT

class MenuManager:
    def __init__(self, font_title, font_large, font_med, font_sm):
        self.font_title = font_title
        self.font_large = font_large
        self.font_med = font_med
        self.font_sm = font_sm
        self.selected_index = 0
        self.tick = 0

    def render_title_menu(self, surface):
        """Renders the main title screen."""
        self.tick += 1
        
        # Backdrop overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 25, 220))
        surface.blit(overlay, (0, 0))

        # Title Card
        title_y = 100
        t_surf = self.font_title.render("GEMMA WORLD", True, TEXT_GOLD)
        sub_surf = self.font_large.render("AI ADAPTIVE PLATFORMER", True, (160, 210, 255))
        tag_surf = self.font_med.render("Gemma 4 as the Brain of the World", True, (200, 180, 255))

        surface.blit(t_surf, ((SCREEN_WIDTH - t_surf.get_width()) // 2, title_y))
        surface.blit(sub_surf, ((SCREEN_WIDTH - sub_surf.get_width()) // 2, title_y + 60))
        surface.blit(tag_surf, ((SCREEN_WIDTH - tag_surf.get_width()) // 2, title_y + 105))

        # Menu options
        options = [
            ("1. PLAY GAME", "Start Nova's journey"),
            ("2. HOW TO PLAY", "Controls, Power-ups & Enemies"),
            ("3. AI BRAIN", "Learn how Gemma controls the world"),
            ("4. SETTINGS", "Configure game options"),
            ("5. QUIT", "Exit to desktop")
        ]

        menu_y = 300
        for i, (opt_title, opt_desc) in enumerate(options):
            is_selected = (i == self.selected_index)
            box_w, box_h = 480, 56
            box_x = (SCREEN_WIDTH - box_w) // 2
            box_y = menu_y + (i * 70)

            # Box background
            b_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            bg_col = (40, 30, 70, 230) if is_selected else (20, 24, 38, 200)
            border_col = (180, 120, 255) if is_selected else (60, 80, 120)
            pygame.draw.rect(b_surf, bg_col, (0, 0, box_w, box_h), border_radius=8)
            pygame.draw.rect(b_surf, border_col, (0, 0, box_w, box_h), width=2 if is_selected else 1, border_radius=8)
            surface.blit(b_surf, (box_x, box_y))

            # Indicator arrow
            prefix = "▶ " if is_selected else "  "
            col = TEXT_GOLD if is_selected else COLOR_WHITE
            text = self.font_med.render(prefix + opt_title, True, col)
            surface.blit(text, (box_x + 24, box_y + 14))

        # Bottom hint
        hint = self.font_sm.render("Use UP / DOWN / 1-4 to Select | ENTER to Confirm", True, (150, 170, 200))
        surface.blit(hint, ((SCREEN_WIDTH - hint.get_width()) // 2, SCREEN_HEIGHT - 60))

    def render_how_to_play(self, surface):
        """Renders controls and item information."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 25, 235))
        surface.blit(overlay, (0, 0))

        card_w, card_h = 920, 560
        cx = (SCREEN_WIDTH - card_w) // 2
        cy = (SCREEN_HEIGHT - card_h) // 2
        pygame.draw.rect(surface, HUD_BG, (cx, cy, card_w, card_h), border_radius=12)
        pygame.draw.rect(surface, (100, 140, 220), (cx, cy, card_w, card_h), width=2, border_radius=12)

        title = self.font_large.render("HOW TO PLAY & CONTROLS", True, TEXT_GOLD)
        surface.blit(title, (cx + (card_w - title.get_width()) // 2, cy + 25))

        lines = [
            ("CONTROLS:", (255, 215, 0)),
            ("  • A / Left Arrow: Run Left", COLOR_WHITE),
            ("  • D / Right Arrow: Run Right", COLOR_WHITE),
            ("  • SPACE: Jump (Hold for high jump, tap for short hop)", COLOR_WHITE),
            ("  • ESC: Pause Game / Return to Menu", COLOR_WHITE),
            ("  • R: Restart level after game over", COLOR_WHITE),
            ("", COLOR_WHITE),
            ("AI DIRECTOR & DEMO TOOLS:", (180, 140, 255)),
            ("  • F3: Toggle Real-Time AI Telemetry & Debug Panel", COLOR_WHITE),
            ("  • F4: DEMO ROGUE AI DECISION (Simulates 1000x Enemies -> Blocked by Validator!)", (255, 140, 140)),
            ("  • F5: Force Immediate Gemma Brain Observation & Decision", COLOR_WHITE),
            ("", COLOR_WHITE),
            ("ORIGINAL POWER-UPS:", (100, 230, 255)),
            ("  • Health Crystal (+35 HP) | Speed Boost (1.5x velocity) | Shield (Absorbs 1 hit)", COLOR_WHITE),
            ("  • Coin Magnet (Draws all nearby coins towards Nova)", COLOR_WHITE)
        ]

        y = cy + 75
        for txt, color in lines:
            t = self.font_sm.render(txt, True, color)
            surface.blit(t, (cx + 40, y))
            y += 26

        btn_hint = self.font_med.render("Press ESC or ENTER to return", True, (150, 210, 255))
        surface.blit(btn_hint, (cx + (card_w - btn_hint.get_width()) // 2, cy + card_h - 45))

    def render_ai_brain_explainer(self, surface):
        """Explains the Observe -> Reason -> Decide -> Validate -> Act pipeline."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 25, 235))
        surface.blit(overlay, (0, 0))

        card_w, card_h = 1000, 580
        cx = (SCREEN_WIDTH - card_w) // 2
        cy = (SCREEN_HEIGHT - card_h) // 2
        pygame.draw.rect(surface, HUD_BG, (cx, cy, card_w, card_h), border_radius=12)
        pygame.draw.rect(surface, AI_ACCENT, (cx, cy, card_w, card_h), width=2, border_radius=12)

        title = self.font_large.render("GEMMA 4: BRAIN OF THE GAME WORLD", True, (210, 180, 255))
        sub = self.font_sm.render("Observe → Reason → Decide → Validate → Act → Recover", True, TEXT_GOLD)
        surface.blit(title, (cx + (card_w - title.get_width()) // 2, cy + 25))
        surface.blit(sub, (cx + (card_w - sub.get_width()) // 2, cy + 60))

        steps = [
            ("1. OBSERVE", "Central GameState records health, deaths, score, and last 10 player events in a clean JSON snapshot."),
            ("2. REASON", "Gemma 4 evaluates the player's pacing, skill, and danger on an asynchronous background thread."),
            ("3. DECIDE", "Gemma outputs a structured JSON decision from 12 strict actions (spawn enemy, spawn powerup, etc.)."),
            ("4. VALIDATE", "Safety validator verifies whitelist, checks limits, and clamps rogue values (e.g., 1000 enemies -> clamped)."),
            ("5. ACT", "Action executor safely applies mutations (spawns items/enemies, changes weather, adjusts difficulty)."),
            ("6. RECOVER", "If Gemma times out (>3.0s) or goes offline, deterministic rule-based fallback takes over seamlessly.")
        ]

        box_w = 900
        box_h = 58
        start_y = cy + 95
        for i, (step_title, step_desc) in enumerate(steps):
            by = start_y + (i * 68)
            b_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            pygame.draw.rect(b_surf, (25, 22, 45, 220), (0, 0, box_w, box_h), border_radius=8)
            pygame.draw.rect(b_surf, (80, 70, 120), (0, 0, box_w, box_h), width=1, border_radius=8)
            surface.blit(b_surf, (cx + 50, by))

            st_surf = self.font_med.render(step_title, True, (255, 215, 0))
            sd_surf = self.font_sm.render(step_desc, True, (220, 230, 245))
            surface.blit(st_surf, (cx + 65, by + 8))
            surface.blit(sd_surf, (cx + 65, by + 30))

        btn_hint = self.font_med.render("Press ESC or ENTER to return", True, (150, 210, 255))
        surface.blit(btn_hint, (cx + (card_w - btn_hint.get_width()) // 2, cy + card_h - 38))
