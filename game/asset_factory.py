"""
Asset Factory for GEMMA WORLD
Procedurally generates high-quality, original retro neo-arcade sprites
for Nova, enemies, tiles, and power-up items.
"""
import pygame
from config import (
    COLOR_NOVA, COLOR_NOVA_ACCENT, COLOR_NOVA_SHIELD,
    COLOR_VENOM, COLOR_JOKER, COLOR_FLASH,
    COLOR_COIN, COLOR_COIN_GLOW,
    COLOR_HEALTH_CRYSTAL, COLOR_SPEED_BOOST, COLOR_SHIELD, COLOR_MAGNET,
    COLOR_GROUND, COLOR_DIRT, COLOR_PLATFORM, COLOR_PLATFORM_ACCENT,
    COLOR_ONEWAY_PLATFORM, COLOR_WHITE, COLOR_BLACK
)

def create_nova_surface(width=40, height=52, facing_right=True, state="idle", frame_tick=0):
    """
    Generates procedural sprite for original protagonist Nova:
    A high-tech cyber explorer with cyan energy suit and golden visor.
    """
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Body bobbing for idle/run
    bob = 0
    if state == "run":
        bob = (frame_tick // 4) % 3
    elif state == "jump":
        bob = -2

    # Outer Energy Aura / Suit Body
    body_rect = pygame.Rect(8, 14 + bob, 24, 28)
    pygame.draw.rect(surf, COLOR_NOVA, body_rect, border_radius=6)
    
    # Cyber Chest Armor
    chest_rect = pygame.Rect(12, 18 + bob, 16, 14)
    pygame.draw.rect(surf, (20, 60, 90), chest_rect, border_radius=3)
    # Energy Core (Pulse)
    pulse_val = 180 + (frame_tick * 8) % 75
    pygame.draw.circle(surf, (pulse_val, 255, 255), (20, 25 + bob), 4)

    # Helmet
    helmet_rect = pygame.Rect(10, 4 + bob, 20, 16)
    pygame.draw.rect(surf, (20, 35, 55), helmet_rect, border_radius=5)
    
    # Visor (Golden neon visor)
    if facing_right:
        visor_rect = pygame.Rect(18, 9 + bob, 12, 6)
    else:
        visor_rect = pygame.Rect(10, 9 + bob, 12, 6)
    pygame.draw.rect(surf, COLOR_NOVA_ACCENT, visor_rect, border_radius=2)

    # Feet / Thrusters
    leg_l = pygame.Rect(10, 42 + bob, 8, 8)
    leg_r = pygame.Rect(22, 42 + bob, 8, 8)
    pygame.draw.rect(surf, (30, 40, 60), leg_l, border_radius=2)
    pygame.draw.rect(surf, (30, 40, 60), leg_r, border_radius=2)

    return surf

def create_enemy_surface(enemy_type="web_hero", width=40, height=40, frame_tick=0):
    """
    Procedurally generates detailed superhero-inspired enemy sprites.
    Primary types: web_hero, blast_hero, dark_hero
    Legacy aliases: armored_hero -> blast_hero, dark_knight -> dark_hero
    """
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    from config import COLOR_WEB_HERO, COLOR_WEB_BLUE, COLOR_ARMORED, COLOR_DARK_KNIGHT, COLOR_THUNDER, COLOR_GREEN_MONSTER, COLOR_SPEED_HERO

    # Alias mapping for backwards compatibility with level JSONs
    alias_map = {
        "armored_hero": "blast_hero",
        "dark_knight": "dark_hero",
    }
    enemy_type = alias_map.get(enemy_type, enemy_type)

    cx, cy = width // 2, height // 2

    if enemy_type == "web_hero":
        # ── Spider-Man inspired: Red/Blue suit, big white eyes, web pattern ──
        # Body (blue base)
        pygame.draw.ellipse(surf, (30, 50, 180), (4, 6, width - 8, height - 10))
        # Red torso overlay
        pygame.draw.ellipse(surf, (200, 30, 30), (8, 4, width - 16, height // 2))
        # Red mask / head area
        pygame.draw.ellipse(surf, (210, 25, 25), (cx - 9, 2, 18, 16))
        # Big white eyes
        pygame.draw.ellipse(surf, (255, 255, 255), (cx - 8, 6, 7, 5))
        pygame.draw.ellipse(surf, (255, 255, 255), (cx + 1, 6, 7, 5))
        # Black eye outline
        pygame.draw.ellipse(surf, (20, 20, 20), (cx - 8, 6, 7, 5), 1)
        pygame.draw.ellipse(surf, (20, 20, 20), (cx + 1, 6, 7, 5), 1)
        # Web pattern lines on torso
        for i in range(3):
            y_off = 12 + i * 7
            pygame.draw.line(surf, (30, 30, 30), (10, y_off), (width - 10, y_off), 1)
        pygame.draw.line(surf, (30, 30, 30), (cx, 4), (cx, height - 8), 1)
        # Legs – blue
        pygame.draw.rect(surf, (30, 50, 180), (cx - 8, height - 12, 6, 10), border_radius=2)
        pygame.draw.rect(surf, (30, 50, 180), (cx + 2, height - 12, 6, 10), border_radius=2)

    elif enemy_type == "blast_hero":
        # ── Iron Man inspired: Red/Gold armor, glowing arc reactor, helmet ──
        # Main armor body – deep red
        pygame.draw.rect(surf, (180, 25, 25), (6, 10, width - 12, height - 16), border_radius=5)
        # Gold trim on shoulders
        pygame.draw.rect(surf, (220, 185, 40), (3, 10, 6, 12), border_radius=2)
        pygame.draw.rect(surf, (220, 185, 40), (width - 9, 10, 6, 12), border_radius=2)
        # Gold belt / waist
        pygame.draw.rect(surf, (220, 185, 40), (8, height // 2 + 2, width - 16, 5), border_radius=2)
        # Helmet – dark red with gold faceplate
        pygame.draw.rect(surf, (160, 20, 20), (cx - 10, 0, 20, 14), border_radius=4)
        pygame.draw.rect(surf, (220, 185, 40), (cx - 6, 3, 12, 8), border_radius=2)
        # Glowing eyes (white slits)
        pygame.draw.rect(surf, (200, 230, 255), (cx - 5, 5, 4, 2))
        pygame.draw.rect(surf, (200, 230, 255), (cx + 1, 5, 4, 2))
        # Arc reactor – pulsing blue/white circle in chest
        pulse = 180 + (frame_tick * 6) % 75
        pygame.draw.circle(surf, (pulse, 240, 255), (cx, cy - 2), 5)
        pygame.draw.circle(surf, (255, 255, 255), (cx, cy - 2), 2)
        # Repulsor circles on hands (tiny glowing dots at sides)
        pygame.draw.circle(surf, (140, 220, 255), (6, cy + 6), 3)
        pygame.draw.circle(surf, (140, 220, 255), (width - 6, cy + 6), 3)
        # Legs – dark red with gold knee accents
        pygame.draw.rect(surf, (160, 20, 20), (cx - 7, height - 14, 6, 12), border_radius=2)
        pygame.draw.rect(surf, (160, 20, 20), (cx + 1, height - 14, 6, 12), border_radius=2)
        pygame.draw.rect(surf, (220, 185, 40), (cx - 7, height - 10, 6, 3), border_radius=1)
        pygame.draw.rect(surf, (220, 185, 40), (cx + 1, height - 10, 6, 3), border_radius=1)
        # Jet boots glow
        glow_alpha = 120 + (frame_tick * 4) % 80
        boot_surf = pygame.Surface((8, 4), pygame.SRCALPHA)
        pygame.draw.ellipse(boot_surf, (100, 180, 255, glow_alpha), (0, 0, 8, 4))
        surf.blit(boot_surf, (cx - 8, height - 4))
        surf.blit(boot_surf, (cx, height - 4))

    elif enemy_type == "dark_hero":
        # ── Batman inspired: Dark cape silhouette, pointed ears, utility belt ──
        # Cape – wide dark triangle behind body
        cape_pts = [(cx, 4), (width + 4, height - 2), (-4, height - 2)]
        pygame.draw.polygon(surf, (20, 20, 30), cape_pts)
        # Inner cape shading
        inner_cape = [(cx, 10), (width - 4, height - 4), (4, height - 4)]
        pygame.draw.polygon(surf, (35, 35, 50), inner_cape)
        # Body – dark grey armor
        pygame.draw.rect(surf, (50, 50, 60), (10, 14, width - 20, height - 22), border_radius=4)
        # Chest emblem (bat silhouette – simplified as a small dark polygon)
        bat_y = cy - 4
        bat_pts = [
            (cx - 6, bat_y), (cx - 8, bat_y - 3), (cx - 4, bat_y - 1),
            (cx, bat_y - 5),
            (cx + 4, bat_y - 1), (cx + 8, bat_y - 3), (cx + 6, bat_y),
            (cx, bat_y + 2)
        ]
        pygame.draw.polygon(surf, (15, 15, 20), bat_pts)
        # Cowl / head with pointed ears
        pygame.draw.ellipse(surf, (25, 25, 35), (cx - 9, 2, 18, 16))
        # Pointed ear left
        pygame.draw.polygon(surf, (25, 25, 35), [(cx - 9, 6), (cx - 12, -2), (cx - 5, 4)])
        # Pointed ear right
        pygame.draw.polygon(surf, (25, 25, 35), [(cx + 9, 6), (cx + 12, -2), (cx + 5, 4)])
        # White eye slits
        pygame.draw.rect(surf, (220, 220, 230), (cx - 6, 8, 5, 3), border_radius=1)
        pygame.draw.rect(surf, (220, 220, 230), (cx + 1, 8, 5, 3), border_radius=1)
        # Utility belt – golden strip at waist
        pygame.draw.rect(surf, (210, 180, 40), (10, cy + 4, width - 20, 4), border_radius=1)
        # Belt pouches
        for bx in range(12, width - 12, 6):
            pygame.draw.rect(surf, (180, 155, 30), (bx, cy + 3, 4, 5), border_radius=1)
        # Legs – dark grey
        pygame.draw.rect(surf, (40, 40, 50), (cx - 7, height - 12, 6, 10), border_radius=2)
        pygame.draw.rect(surf, (40, 40, 50), (cx + 1, height - 12, 6, 10), border_radius=2)

    elif enemy_type == "thunder_hero":
        pygame.draw.rect(surf, (30, 30, 40), (4, 4, width-8, height-8), border_radius=8)
        pygame.draw.circle(surf, (200, 200, 200), (cx, cy - 4), 10)
        pts = [(cx + 2, cy - 8), (cx - 4, cy), (cx + 2, cy), (cx - 2, cy + 8)]
        pygame.draw.lines(surf, COLOR_THUNDER, False, pts, 2)

    elif enemy_type == "green_monster":
        pygame.draw.rect(surf, COLOR_GREEN_MONSTER, (0, 10, width, height-10), border_radius=6)
        pygame.draw.rect(surf, (100, 50, 150), (2, height//2 + 4, width-4, height//2 - 4))

    elif enemy_type == "speed_hero":
        pygame.draw.ellipse(surf, COLOR_SPEED_HERO, (0, height//2 - 6, width, 12))
        pygame.draw.circle(surf, (255, 200, 50), (cx + 4, cy), 4)

    return surf


def create_item_surface(item_type="coin", size=28, frame_tick=0):
    """Generates procedural sprite for collectibles and power-ups."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    if item_type == "coin":
        # Rotating golden coin
        scale_x = abs(round(size * 0.4 * abs(((frame_tick % 30) - 15) / 15.0))) + 4
        rect = pygame.Rect(center - scale_x, 3, scale_x * 2, size - 6)
        pygame.draw.ellipse(surf, COLOR_COIN, rect)
        pygame.draw.ellipse(surf, COLOR_COIN_GLOW, (center - scale_x + 2, 5, max(1, scale_x * 2 - 4), size - 10))

    elif item_type == "health_crystal":
        # Green rhomboid health crystal
        pts = [(center, 2), (size - 4, center), (center, size - 2), (4, center)]
        pygame.draw.polygon(surf, COLOR_HEALTH_CRYSTAL, pts)
        inner_pts = [(center, 6), (size - 8, center), (center, size - 6), (8, center)]
        pygame.draw.polygon(surf, (180, 255, 210), inner_pts)

    elif item_type == "speed_boost":
        # Cyan lightning bolt
        pts = [(16, 2), (6, 15), (14, 15), (10, 26), (22, 12), (15, 12)]
        pygame.draw.polygon(surf, COLOR_SPEED_BOOST, pts)
        pygame.draw.lines(surf, COLOR_WHITE, False, pts, 1)

    elif item_type == "shield":
        # Cobalt crest shield
        pts = [(center, 2), (size - 3, 7), (size - 5, 20), (center, size - 2), (5, 20), (3, 7)]
        pygame.draw.polygon(surf, COLOR_SHIELD, pts)
        pygame.draw.lines(surf, (200, 220, 255), True, pts, 2)

    elif item_type == "magnet":
        # Horseshoe magnet
        rect = pygame.Rect(4, 4, size - 8, size - 8)
        pygame.draw.arc(surf, COLOR_MAGNET, rect, 0, 3.14, 6)
        pygame.draw.rect(surf, (240, 240, 240), (4, center, 6, 8))
        pygame.draw.rect(surf, (240, 240, 240), (size - 10, center, 6, 8))

    return surf

def create_platform_surface(width, height, platform_type="solid"):
    """Generates procedural platform tiles."""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    
    if platform_type == "ground":
        # Top grass border
        pygame.draw.rect(surf, COLOR_GROUND, (0, 0, width, 10))
        # Dirt underfill with stone flecks
        pygame.draw.rect(surf, COLOR_DIRT, (0, 10, width, height - 10))
        # Subtle texture lines
        for x in range(12, width, 32):
            pygame.draw.rect(surf, (80, 50, 25), (x, 14, 8, 6), border_radius=2)

    elif platform_type == "floating":
        # Tech-metal floating platform
        pygame.draw.rect(surf, COLOR_PLATFORM, (0, 0, width, height), border_radius=4)
        pygame.draw.rect(surf, COLOR_PLATFORM_ACCENT, (0, 0, width, 4), border_top_left_radius=4, border_top_right_radius=4)
        pygame.draw.rect(surf, (40, 50, 70), (0, 0, width, height), width=2, border_radius=4)

    elif platform_type == "oneway":
        # Golden semi-permeable beam
        pygame.draw.rect(surf, COLOR_ONEWAY_PLATFORM, (0, 0, width, height), border_radius=3)
        for x in range(0, width, 16):
            pygame.draw.line(surf, (240, 225, 140), (x, 0), (x + 8, height), 2)

    return surf
