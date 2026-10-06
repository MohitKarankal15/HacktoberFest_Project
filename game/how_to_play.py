import pygame
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, TEXT_GOLD, FPS, AI_ACCENT
from game.asset_factory import create_nova_surface, create_enemy_surface

class HowToPlayDemo:
    def __init__(self, font_large, font_med, font_sm):
        self.font_large = font_large
        self.font_med = font_med
        self.font_sm = font_sm
        self.active_demo = None
        self.time_elapsed = 0.0
        self.selected_index = 0

        self.options = [
            ("MOVEMENT DEMO", "movement"),
            ("JUMP DEMO", "jump"),
            ("WEB ATTACK DEMO", "web"),
            ("BLAST ATTACK DEMO", "blast"),
            ("BATARANG ATTACK DEMO", "batarang"),
            ("GEMMA AI DEMO", "gemma"),
            ("BACK TO MENU", "back")
        ]

        self.player_img = create_nova_surface(40, 52)
        self.web_hero_img = create_enemy_surface("web_hero", 40, 52)
        self.blast_hero_img = create_enemy_surface("blast_hero", 40, 52)
        self.dark_hero_img = create_enemy_surface("dark_hero", 40, 52)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.active_demo:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                        self.active_demo = None
                        self.time_elapsed = 0.0
                else:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        choice = self.options[self.selected_index][1]
                        if choice == "back":
                            return "back"
                        else:
                            self.active_demo = choice
                            self.time_elapsed = 0.0
                    elif event.key == pygame.K_ESCAPE:
                        return "back"
        return None

    def update(self, dt):
        if self.active_demo:
            self.time_elapsed += dt
            if self.time_elapsed > 5.0: # Auto return after 5 seconds
                self.active_demo = None
                self.time_elapsed = 0.0

    def draw(self, surface):
        surface.fill((10, 14, 25))

        if not self.active_demo:
            title = self.font_large.render("HOW TO PLAY & CONTROLS", True, TEXT_GOLD)
            surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 50))

            start_y = 150
            for i, (text, action) in enumerate(self.options):
                is_selected = (i == self.selected_index)
                color = TEXT_GOLD if is_selected else COLOR_WHITE
                prefix = "▶ " if is_selected else "  "
                opt_surf = self.font_med.render(prefix + text, True, color)
                surface.blit(opt_surf, ((SCREEN_WIDTH - 400) // 2, start_y + i * 50))

            hint = self.font_sm.render("Use UP/DOWN to select, ENTER to view demo", True, (150, 170, 200))
            surface.blit(hint, ((SCREEN_WIDTH - hint.get_width()) // 2, SCREEN_HEIGHT - 60))

        else:
            # Draw the active demo
            self._draw_demo(surface)

    def _draw_demo(self, surface):
        t = self.time_elapsed
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Ground
        pygame.draw.rect(surface, (50, 50, 50), (100, cy + 50, SCREEN_WIDTH - 200, 20))

        if self.active_demo == "movement":
            x_offset = math.sin(t * 3) * 100
            surface.blit(self.player_img, (cx + x_offset - 20, cy))
            
            txt = self.font_med.render("A / D or LEFT / RIGHT to Move", True, COLOR_WHITE)
            surface.blit(txt, ((SCREEN_WIDTH - txt.get_width()) // 2, cy - 100))

        elif self.active_demo == "jump":
            y_offset = -abs(math.sin(t * 4)) * 100
            x_offset = (t % 2.0) * 100 - 50
            surface.blit(self.player_img, (cx + x_offset - 20, cy + y_offset))
            
            txt = self.font_med.render("SPACE to Jump (Can move while jumping!)", True, COLOR_WHITE)
            surface.blit(txt, ((SCREEN_WIDTH - txt.get_width()) // 2, cy - 100))

        elif self.active_demo == "web":
            surface.blit(self.web_hero_img, (cx - 150, cy))
            surface.blit(self.player_img, (cx + 100, cy))
            
            if (t % 1.5) > 0.5:
                # web flying
                pygame.draw.circle(surface, (200, 200, 200), (int(cx - 100 + (t*400)%250), cy + 25), 8)
                
            if (t % 1.5) > 1.0:
                txt = self.font_med.render("PLAYER SLOWED!", True, (150, 150, 255))
                surface.blit(txt, (cx + 60, cy - 40))

            desc = self.font_med.render("Web attack slows you temporarily.", True, COLOR_WHITE)
            surface.blit(desc, ((SCREEN_WIDTH - desc.get_width()) // 2, cy - 100))

        elif self.active_demo == "blast":
            surface.blit(self.blast_hero_img, (cx - 150, cy))
            surface.blit(self.player_img, (cx + 100 + (20 if (t%1.5)>1.0 else 0), cy))
            
            if (t % 1.5) > 0.5:
                pygame.draw.circle(surface, (255, 100, 0), (int(cx - 100 + (t*500)%250), cy + 25), 10)
                
            if (t % 1.5) > 1.0:
                txt = self.font_med.render("DAMAGE + KNOCKBACK!", True, (255, 100, 100))
                surface.blit(txt, (cx + 60, cy - 40))

            desc = self.font_med.render("Dodge energy blasts.", True, COLOR_WHITE)
            surface.blit(desc, ((SCREEN_WIDTH - desc.get_width()) // 2, cy - 100))

        elif self.active_demo == "batarang":
            surface.blit(self.dark_hero_img, (cx - 150, cy))
            surface.blit(self.player_img, (cx + 100, cy))
            
            if (t % 1.0) > 0.3:
                pygame.draw.rect(surface, (100, 100, 100), (int(cx - 100 + (t*800)%250), cy + 20, 15, 5))
                
            if (t % 1.0) > 0.7:
                txt = self.font_med.render("STUNNED!", True, (200, 200, 100))
                surface.blit(txt, (cx + 80, cy - 40))

            desc = self.font_med.render("Watch for fast projectiles.", True, COLOR_WHITE)
            surface.blit(desc, ((SCREEN_WIDTH - desc.get_width()) // 2, cy - 100))
            
        elif self.active_demo == "gemma":
            # AI Demo UI
            pygame.draw.rect(surface, (20, 20, 40), (cx - 200, cy - 120, 400, 280), border_radius=10)
            pygame.draw.rect(surface, AI_ACCENT, (cx - 200, cy - 120, 400, 280), width=2, border_radius=10)
            
            t1 = self.font_med.render("GEMMA 4 BRAIN", True, TEXT_GOLD)
            surface.blit(t1, (cx - 180, cy - 100))
            
            stage = int(t % 4.0)
            
            if stage >= 0:
                s1 = self.font_sm.render("OBSERVING... Player Health: 25%", True, COLOR_WHITE)
                surface.blit(s1, (cx - 180, cy - 50))
            if stage >= 1:
                s2 = self.font_sm.render("REASONING: Player is struggling.", True, (200, 200, 255))
                surface.blit(s2, (cx - 180, cy - 20))
            if stage >= 2:
                s3 = self.font_sm.render("DECISION: Spawn Health Power-up", True, (150, 255, 150))
                surface.blit(s3, (cx - 180, cy + 10))
            if stage >= 3:
                s4 = self.font_med.render("✓ VALIDATED & EXECUTED", True, TEXT_GOLD)
                surface.blit(s4, (cx - 180, cy + 60))
                
            desc = self.font_med.render("GEMMA IS THE GAME DIRECTOR", True, COLOR_WHITE)
            surface.blit(desc, ((SCREEN_WIDTH - desc.get_width()) // 2, cy - 180))

        hint = self.font_sm.render("Press SPACE to return", True, (150, 150, 150))
        surface.blit(hint, ((SCREEN_WIDTH - hint.get_width()) // 2, SCREEN_HEIGHT - 40))
