"""
F3 Developer & AI Telemetry Debug Panel for GEMMA WORLD
Displays real-time Gemma status, latency, decisions, validation status, and history.
"""
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, HUD_BG, HUD_BORDER, TEXT_GOLD, HEALTH_RED

def draw_debug_panel(surface, gemma_brain, state_manager, font_med, font_sm):
    """Renders the AI Telemetry HUD overlay on the screen."""
    panel_w = 420
    panel_h = 490
    panel_x = SCREEN_WIDTH - panel_w - 20
    panel_y = 110

    # Background card
    panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    pygame.draw.rect(panel_surf, (15, 18, 30, 235), (0, 0, panel_w, panel_h), border_radius=12)
    pygame.draw.rect(panel_surf, (140, 90, 255), (0, 0, panel_w, panel_h), width=2, border_radius=12)
    surface.blit(panel_surf, (panel_x, panel_y))

    # Header
    header = font_med.render("⚡ GEMMA 4 AI DIRECTOR TELEMETRY", True, (210, 180, 255))
    surface.blit(header, (panel_x + 16, panel_y + 14))
    pygame.draw.line(surface, (80, 60, 130), (panel_x + 16, panel_y + 42), (panel_x + panel_w - 16, panel_y + 42), 1)

    y_offset = panel_y + 52

    # 1. Gemma Status
    status_color = (100, 255, 150) if "Connected" in gemma_brain.status or "Online" in gemma_brain.status else (255, 200, 80)
    stat_lbl = font_sm.render(f"GEMMA STATUS: ", True, (180, 190, 210))
    stat_val = font_sm.render(gemma_brain.status, True, status_color)
    surface.blit(stat_lbl, (panel_x + 16, y_offset))
    surface.blit(stat_val, (panel_x + 16 + stat_lbl.get_width(), y_offset))
    y_offset += 24

    # 2. AI Latency
    lat_color = (120, 255, 120) if gemma_brain.last_latency < 1.0 else (255, 220, 100)
    lat_lbl = font_sm.render("AI LATENCY: ", True, (180, 190, 210))
    lat_val = font_sm.render(f"{gemma_brain.last_latency:.2f} seconds", True, lat_color)
    surface.blit(lat_lbl, (panel_x + 16, y_offset))
    surface.blit(lat_val, (panel_x + 16 + lat_lbl.get_width(), y_offset))
    y_offset += 24

    # 3. Last Decision
    action_name = gemma_brain.last_decision.get("action", "None") if gemma_brain.last_decision else "None"
    dec_lbl = font_sm.render("LAST DECISION: ", True, (180, 190, 210))
    dec_val = font_sm.render(action_name, True, TEXT_GOLD)
    surface.blit(dec_lbl, (panel_x + 16, y_offset))
    surface.blit(dec_val, (panel_x + 16 + dec_lbl.get_width(), y_offset))
    y_offset += 24

    # 4. Decision Status (Validation)
    val_status = gemma_brain.last_validation_status
    vcolor = (100, 255, 150) if val_status == "ACCEPTED" else ((255, 180, 50) if val_status == "CLAMPED" else HEALTH_RED)
    v_lbl = font_sm.render("DECISION: ", True, (180, 190, 210))
    v_val = font_sm.render(val_status, True, vcolor)
    surface.blit(v_lbl, (panel_x + 16, y_offset))
    surface.blit(v_val, (panel_x + 16 + v_lbl.get_width(), y_offset))
    y_offset += 24

    # 5. Current Difficulty
    diff_lbl = font_sm.render(f"CURRENT DIFFICULTY: {state_manager.difficulty}/10", True, (210, 170, 255))
    surface.blit(diff_lbl, (panel_x + 16, y_offset))
    y_offset += 24

    # 6. Gemma's Stated Reason (Wrapped)
    r_lbl = font_sm.render("REASON:", True, (180, 190, 210))
    surface.blit(r_lbl, (panel_x + 16, y_offset))
    y_offset += 20
    # Render reason truncated/wrapped
    reason_text = gemma_brain.last_reason[:55] + ("..." if len(gemma_brain.last_reason) > 55 else "")
    r_val = font_sm.render(f'"{reason_text}"', True, (220, 220, 240))
    surface.blit(r_val, (panel_x + 20, y_offset))
    y_offset += 28

    # 7. Decision History Section
    pygame.draw.line(surface, (60, 50, 90), (panel_x + 16, y_offset), (panel_x + panel_w - 16, y_offset), 1)
    y_offset += 8
    hist_title = font_sm.render("DECISION HISTORY:", True, (180, 190, 210))
    surface.blit(hist_title, (panel_x + 16, y_offset))
    y_offset += 22

    for ts, act, st in reversed(gemma_brain.decision_history[-5:]):
        st_color = (120, 255, 140) if st == "ACCEPTED" else ((255, 190, 60) if st == "CLAMPED" else HEALTH_RED)
        line_txt = f"[{ts}] {act[:22]} → "
        t_surf = font_sm.render(line_txt, True, (170, 180, 200))
        s_surf = font_sm.render(st, True, st_color)
        surface.blit(t_surf, (panel_x + 20, y_offset))
        surface.blit(s_surf, (panel_x + 20 + t_surf.get_width(), y_offset))
        y_offset += 20

    # Controls guide at bottom
    pygame.draw.line(surface, (60, 50, 90), (panel_x + 16, panel_y + panel_h - 48), (panel_x + panel_w - 16, panel_y + panel_h - 48), 1)
    hint1 = font_sm.render("[F3] Hide Panel | [F4] Rogue Demo (1000x Enemies)", True, (150, 160, 190))
    hint2 = font_sm.render("[F5] Force Gemma Query Now", True, (150, 160, 190))
    surface.blit(hint1, (panel_x + 16, panel_y + panel_h - 42))
    surface.blit(hint2, (panel_x + 16, panel_y + panel_h - 22))
