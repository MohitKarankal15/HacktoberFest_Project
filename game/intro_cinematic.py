import pygame
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, TEXT_GOLD, FPS, AI_ACCENT
from game.asset_factory import create_enemy_surface

class IntroCinematic:
    def __init__(self, font_title, font_large, font_med, font_sm):
        self.font_title = font_title
        self.font_large = font_large
        self.font_med = font_med
        self.font_sm = font_sm
        self.time_elapsed = 0.0
        self.is_finished = False

        self.web_hero_img = create_enemy_surface("web_hero", 40, 52)
        self.blast_hero_img = create_enemy_surface("blast_hero", 40, 52)
        self.dark_hero_img = create_enemy_surface("dark_hero", 40, 52)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                    self.is_finished = True

    def update(self, dt):
        self.time_elapsed += dt
        if self.time_elapsed > 25.0:
            self.is_finished = True

    def draw(self, surface):
        surface.fill((10, 12, 20))
        t = self.time_elapsed

        # Skip hint
        skip_txt = self.font_sm.render("Press SPACE/ENTER/ESC to skip", True, (150, 150, 150))
        surface.blit(skip_txt, (SCREEN_WIDTH - skip_txt.get_width() - 20, 20))

        if t < 4.0:
            # SCENE 1: WORLD INTRO
            alpha = min(255, int((t / 1.0) * 255)) if t < 1.0 else (min(255, int(((4.0 - t) / 1.0) * 255)) if t > 3.0 else 255)
            t1 = self.font_title.render("GEMMA WORLD", True, TEXT_GOLD)
            t2 = self.font_large.render("An AI-powered adaptive platformer", True, COLOR_WHITE)
            t3 = self.font_med.render("OBSERVE • THINK • DECIDE • ACT", True, AI_ACCENT)
            t1.set_alpha(alpha)
            t2.set_alpha(alpha)
            t3.set_alpha(alpha)
            surface.blit(t1, ((SCREEN_WIDTH - t1.get_width()) // 2, 250))
            surface.blit(t2, ((SCREEN_WIDTH - t2.get_width()) // 2, 330))
            surface.blit(t3, ((SCREEN_WIDTH - t3.get_width()) // 2, 380))

        elif t < 8.0:
            # SCENE 2: PLAYER
            alpha = min(255, int(((t - 4.0) / 0.5) * 255)) if t < 4.5 else (min(255, int(((8.0 - t) / 0.5) * 255)) if t > 7.5 else 255)
            t1 = self.font_large.render("YOU CONTROL THE HERO", True, TEXT_GOLD)
            t2 = self.font_med.render("A / LEFT -> Move Left", True, COLOR_WHITE)
            t3 = self.font_med.render("D / RIGHT -> Move Right", True, COLOR_WHITE)
            t4 = self.font_med.render("SPACE -> Jump", True, COLOR_WHITE)
            t1.set_alpha(alpha)
            t2.set_alpha(alpha)
            t3.set_alpha(alpha)
            t4.set_alpha(alpha)
            surface.blit(t1, ((SCREEN_WIDTH - t1.get_width()) // 2, 200))
            surface.blit(t2, ((SCREEN_WIDTH - t2.get_width()) // 2, 280))
            surface.blit(t3, ((SCREEN_WIDTH - t3.get_width()) // 2, 320))
            surface.blit(t4, ((SCREEN_WIDTH - t4.get_width()) // 2, 360))

        elif t < 13.0:
            # SCENE 3: ENEMIES
            alpha = min(255, int(((t - 8.0) / 0.5) * 255)) if t < 8.5 else (min(255, int(((13.0 - t) / 0.5) * 255)) if t > 12.5 else 255)
            t1 = self.font_large.render("BEWARE THE ROGUE HEROES", True, (255, 100, 100))
            t1.set_alpha(alpha)
            surface.blit(t1, ((SCREEN_WIDTH - t1.get_width()) // 2, 100))

            bx = SCREEN_WIDTH // 4
            by = 250
            # Web
            surface.blit(self.web_hero_img, (bx - 20, by))
            wt = self.font_sm.render("WEB HERO (Slows you)", True, COLOR_WHITE)
            wt.set_alpha(alpha)
            surface.blit(wt, (bx - wt.get_width()//2, by + 60))

            # Blast
            bx += SCREEN_WIDTH // 4
            surface.blit(self.blast_hero_img, (bx - 20, by))
            bt = self.font_sm.render("BLAST HERO (Knockback)", True, COLOR_WHITE)
            bt.set_alpha(alpha)
            surface.blit(bt, (bx - bt.get_width()//2, by + 60))

            # Dark
            bx += SCREEN_WIDTH // 4
            surface.blit(self.dark_hero_img, (bx - 20, by))
            dt = self.font_sm.render("DARK HERO (Stuns)", True, COLOR_WHITE)
            dt.set_alpha(alpha)
            surface.blit(dt, (bx - dt.get_width()//2, by + 60))

        elif t < 18.0:
            # SCENE 4: GEMMA BRAIN
            alpha = min(255, int(((t - 13.0) / 0.5) * 255)) if t < 13.5 else (min(255, int(((18.0 - t) / 0.5) * 255)) if t > 17.5 else 255)
            msgs = []
            if t > 13.5: msgs.append("GEMMA OBSERVES THE WORLD")
            if t > 14.5: msgs.append("GEMMA THINKS & REASONS")
            if t > 15.5: msgs.append("GEMMA DECIDES")
            if t > 16.5: msgs.append("THE WORLD REACTS")
            
            y = 200
            for m in msgs:
                surf = self.font_large.render(m, True, AI_ACCENT)
                surf.set_alpha(alpha)
                surface.blit(surf, ((SCREEN_WIDTH - surf.get_width()) // 2, y))
                y += 60

        elif t < 22.0:
            # SCENE 5 & 6: SAFETY
            alpha = min(255, int(((t - 18.0) / 0.5) * 255)) if t < 18.5 else (min(255, int(((22.0 - t) / 0.5) * 255)) if t > 21.5 else 255)
            t1 = self.font_large.render("SAFETY VALIDATOR", True, TEXT_GOLD)
            t2 = self.font_med.render("Gemma: Spawn 100 Enemies", True, (255, 100, 100))
            t3 = self.font_med.render("Validator: INVALID DECISION. CLAMPING TO SAFE LIMIT.", True, COLOR_WHITE)
            t4 = self.font_med.render("AI decisions are strictly verified before execution.", True, AI_ACCENT)
            
            for s, y_pos in [(t1, 150), (t2, 250), (t3, 300), (t4, 400)]:
                s.set_alpha(alpha)
                surface.blit(s, ((SCREEN_WIDTH - s.get_width()) // 2, y_pos))

        elif t < 25.0:
            # SCENE 7: FINAL TITLE
            alpha = min(255, int(((t - 22.0) / 1.0) * 255))
            t1 = self.font_title.render("GEMMA WORLD", True, TEXT_GOLD)
            t2 = self.font_large.render("Where AI controls the world.", True, COLOR_WHITE)
            t3 = self.font_med.render("PRESS ANY KEY TO START", True, AI_ACCENT)
            
            t1.set_alpha(alpha)
            t2.set_alpha(alpha)
            t3.set_alpha(alpha)
            surface.blit(t1, ((SCREEN_WIDTH - t1.get_width()) // 2, 250))
            surface.blit(t2, ((SCREEN_WIDTH - t2.get_width()) // 2, 330))
            
            # Pulse
            if math.sin(t * 10) > 0:
                surface.blit(t3, ((SCREEN_WIDTH - t3.get_width()) // 2, 450))

